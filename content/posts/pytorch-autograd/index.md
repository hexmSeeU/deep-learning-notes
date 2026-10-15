{
  "title": "PyTorch autograd：计算图、梯度与几个容易混淆的开关",
  "description": "第一章 · 第 7 篇。从普通函数出发，看清前向记录、反向执行与梯度保存，区分 no_grad、detach、retain_graph 和 create_graph。",
  "date": "2026-10-15T22:38:50+08:00",
  "slug": "pytorch-autograd",
  "categories": ["基础"],
  "tags": ["PyTorch", "自动求导", "计算图", "梯度"],
  "draft": false
}

前面已经讨论过[链式法则]({{< relref "/posts/chain-rule-and-computational-graphs" >}})和[反向传播]({{< relref "/posts/backpropagation" >}})。这篇不再重新推导基础规则，而是回答：**PyTorch 怎样记录计算、执行求导，又把结果放在哪里？**

讨论中最容易混在一起的是三件事：

1. **记录关系**：哪些运算被记录为可求导的路径？
2. **执行计算**：有没有真正沿路径反向计算？
3. **保存结果**：梯度是累加到 `.grad`，还是直接返回？

下面继续只用普通函数。每段独立示例都从新建张量开始；跨段复用旧变量可能遇到梯度累加或图已释放的问题。

## 1. requires_grad 负责标记，backward 负责执行

```python
import torch

x = torch.tensor(2.0, requires_grad=True)
y = x ** 2

print(y)       # tensor(4., grad_fn=...)
print(x.grad)  # None

y.backward()
print(x.grad)  # tensor(4.)
print(x)       # 值仍是 2
```

创建 x 时，`requires_grad=True` 标记它需要梯度。随后，在正常记录梯度的环境中，`x ** 2` 会建立相应的反向计算关系，并保存或引用求导需要的信息。

**前向计算不是提前算好梯度。** 此时只是算出 y，并为之后的求导做好记录；`x.grad is None` 表示没有保存梯度结果，不表示导数为零。

执行 `y.backward()` 时，autograd 引擎从这个标量输出出发，以 `dy/dy=1` 为起点，沿已记录的连接调用各节点实现好的反向规则：

```text
前向：x=2 ──平方──→ y=4

反向：从 y 的 1 开始
            ↓
      平方的反向规则
      上游导数 × 2x
            ↓
          1×2×2=4
            ↓
      累加到 x.grad
```

它不需要重新阅读 Python 代码，也不是把整个函数重新做一遍符号推导。平方、乘法等运算有各自实现好的反向规则，引擎负责按图组织执行。求导结束后，x 的值不会自动改变。

## 2. grad_fn：反向计算图中的节点

`grad_fn` 是属性，通常写作 `y.grad_fn`，不是 `y.grad_fn()`。它指向与生成该张量的运算对应的反向节点，**不是已经算好的梯度**。

```python
x = torch.tensor(2.0, requires_grad=True)
u = x ** 2
y = 3 * u

print(x.grad_fn)  # None
print(u.grad_fn)  # <PowBackward0 ...>
print(y.grad_fn)  # <MulBackward0 ...>
```

节点名称的具体后缀可能随实现变化，关注平方与乘法的含义即可。

```text
前向：x ──平方──→ u ──乘 3──→ y

反向：x ←── PowBackward ←── MulBackward ←── 起始导数 1
             乘 2x            乘 3
```

`next_functions` 可以进一步观察反向节点的连接：

```python
print(y.grad_fn.next_functions)
# 通常类似：((<PowBackward0 ...>, 0), (None, 0))

print(u.grad_fn.next_functions)
# 通常类似：((<AccumulateGrad ...>, 0),)
```

```text
          y 的 MulBackward
           /            
  u 的 PowBackward      None：常数 3 不需要梯度
          │
    AccumulateGrad
          │
      累加到 x.grad
```

这里先看每对里的第一个元素，后面的索引无需展开。常数 3 的分支是 `None`，表示不需要向它求梯度；**给 u 传回梯度时，依然要用这个 3。**

x 是直接创建的叶子张量，没有生成它的运算，所以 `x.grad_fn` 是 `None`。但反向图中仍有负责向它累加梯度的 `AccumulateGrad` 节点。观察这些连接是为了理解机制，日常使用不需要手动遍历它们。

## 3. 参与求导，不等于自己的 .grad 会被保存

```python
x = torch.tensor(1.0, requires_grad=True)
u = 2 * x + 1
y = u ** 2

y.backward()
print(x.grad)  # tensor(12.)
```

此时 u=3。反向先算 `dy/du=6`，再算 `dy/dx=6×2=12`。

但默认情况下，u 这样的**非叶子张量**不保留自己的 `.grad`。它参与了反向计算，只是中间梯度用完后不默认留在这个属性中。直接读取它的 `.grad` 通常还会出现提示。

如果确实需要观察中间梯度，在反向之前调用 `retain_grad()`：

```python
x = torch.tensor(1.0, requires_grad=True)
u = 2 * x + 1
y = u ** 2

u.retain_grad()
y.backward()

print(u.grad)  # tensor(6.)
print(x.grad)  # tensor(12.)
```

它只要求保存结果，不改变前向数值、导数规则或 u 的非叶子身份。

**“叶子”与“参数”也不是同一个概念。** 叶子描述图中的身份；参数描述我们打算调整的量。输入 x 可以是需要梯度的叶子，却并不需要更新。常规可学习参数通常是叶子，但实际使用的权重也可以由叶子参数计算得到：

```python
raw = torch.nn.Parameter(torch.tensor(2.0))
weight = raw ** 2
y = 3 * weight

y.backward()
print(raw.grad)  # tensor(12.)
```

这里 raw 是独立参数，weight 是非叶子的有效权重。通常调整 raw，再重新计算 weight，间接改变实际权重。不能仅凭“它参与求导”就决定要更新它。

## 4. .grad 会累加；清空结果不会关闭求导

```python
x = torch.tensor(2.0, requires_grad=True)

(x ** 2).backward()
print(x.grad)  # tensor(4.)

(3 * x).backward()
print(x.grad)  # tensor(7.)：之前的 4 + 这次的 3
```

第二次函数对 x 的导数是 3，保存的结果却是 7。原因是 `.grad` 默认累加，而非每次覆盖。

只保留下一次的结果，可以先清空：

```python
x.grad = None
(3 * x).backward()
print(x.grad)  # tensor(3.)
```

`x.grad = None` 不会改变 x 的数值或 `requires_grad` 标记。已有梯度时，`x.grad.zero_()` 也能清零，但保留的是一个零张量；对 `None` 不能调用它。在优化器管理参数的场景里，讨论过的对应写法是 `optimizer.zero_grad(set_to_none=True)`。

### retain_graph 与 retain_grad 不同

对于平方这个例子，默认第一次反向后，求导所需的已保存信息会被释放；直接再次对同一个 y 反向会报错。这里不能笼统理解为所有图对象都消失了。

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2

y.backward(retain_graph=True)
print(x.grad)  # tensor(4.)

y.backward()
print(x.grad)  # tensor(8.)
```

第一次保留了再次反向所需的信息，第二次仍算出导数 4，并累加到原来的 4 上。**翻倍的是保存结果，不是导数，也不是在计算二阶导数。** 两次之间清空 `x.grad`，第二次保存的就仍是 4。

- `retain_grad()`：要求保存某个中间张量的梯度结果。
- `retain_graph=True`：保留原图反向计算所需的信息，方便再次使用。
- 清空 `.grad`：只清除结果，不会恢复已经释放的求导信息。

另一种方式是重新执行前向，得到新的计算图，再对新输出求导。

## 5. no_grad：这段计算从一开始就不记录

```python
x = torch.tensor(2.0, requires_grad=True)

with torch.no_grad():
    u = x ** 2

v = 3 * x
y = u + v
y.backward()

print(y)       # 值是 10
print(x.grad)  # tensor(3.)
```

前向计算时 u=4、v=6，两者都参与了相加。但反向图只记录了经过 v 回到 x 的路径：

```text
前向数值：
x=2 ···平方，不记录···→ u=4 ──┐
                              ├──相加──→ y=10
x=2 ───乘 3，记录─────→ v=6 ──┘

反向贡献：
y ──1──→ v ──乘 3──→ x：贡献 3
y ──1──→ u             到这里停止，没有回到 x 的路径
```

普通数学函数 `x²+3x` 在 x=2 处的导数是 7。这里 autograd 得到 3，是因为我们主动让平方这条路径不参与求导。**参与前向取值，不等于存在反向连接。**

`no_grad` 没有改掉 x 的 `requires_grad=True`。离开这个范围后，`v=3*x` 又会正常记录；此前没有记录的 u 路径不会自动补回来。

## 6. detach：从已有张量得到断开求导关系的张量

```python
x = torch.tensor(2.0, requires_grad=True)
u = x ** 2
d = u.detach()
v = 3 * x

y = d + v
y.backward()
print(x.grad)  # tensor(3.)
```

这次平方运算原本记录了关系，但 d 不再连接到那条求导路径：

```text
x ──平方，记录──→ u
                  │
                detach
                  ↓
                  d ──┐
                      ├──相加──→ y
x ──乘 3───────→ v ──┘

反向：经过 v 回到 x；经过 d 的分支停止。
```

**detach 没有删除 u 原来的图。** 如果在独立的新例子中改用 `y=u+v`，两条路径都会贡献，x 的梯度就是 `2x+3=7`。关键是后续使用 u 还是 d。另一个细节是：detach 得到的张量与原张量共享底层存储，并不是数值的独立副本。

### u = u.detach() 与 no_grad 一样吗？

对于后续仅通过这个 u 求导的代码，效果相似：都没有经过 u 回到 x 的路径。但发生的过程不同：

```python
# 从一开始不记录
with torch.no_grad():
    u = x ** 2

# 先记录，再让变量名 u 指向断开的张量
u = x ** 2
u = u.detach()
```

赋值改变了 Python 变量名指向的对象，不是在原图上执行删除操作：

```python
u = x ** 2
original_u = u
u = u.detach()
# original_u 仍指向原来带求导关系的张量
```

当没有其他引用需要原图时，相关对象才可能被回收。

### grad_fn 为 None，能判断什么？

| 张量 | `requires_grad` | `grad_fn` |
| --- | --- | --- |
| 直接创建的 x | `True` | `None` |
| 正常计算的 `u=x**2` | `True` | `PowBackward…` |
| `d=u.detach()` | `False` | `None` |
| `no_grad` 中计算的 `v=x**2` | `False` | `None` |

所以仅凭 `grad_fn is None`，既不能断定张量来自 detach，也不能断定它不需要梯度。需要结合 `requires_grad` 与创建过程判断。

## 7. 输出有多个元素，从哪里开始反向？

```python
x = torch.tensor([1., 2., 3.], requires_grad=True)
y = x ** 2  # [1, 4, 9]
```

这里直接 `y.backward()` 会报错：y 有三个元素，不能省略起始梯度。我们可以先明确要对哪个标量函数求导：

```python
s = y.sum()
s.backward()
print(x.grad)  # tensor([2., 4., 6.])
```

```text
              s = y[0] + y[1] + y[2]
               /         |         
           传回 1     传回 1     传回 1
             ↓           ↓           ↓
           x[0]²       x[1]²       x[2]²
             ↓           ↓           ↓
           乘 2x[0]    乘 2x[1]    乘 2x[2]
```

如果独立重算并换成 `y.mean().backward()`，每条分支起始传回 1/3，最终梯度就是原来的 1/3，即 `[2/3, 4/3, 2]`。sum 与 mean 指定了不同函数，不能只当成让代码运行的处理。

也可以直接提供起始梯度：

```python
x = torch.tensor([1., 2., 3.], requires_grad=True)
y = x ** 2

y.backward(gradient=torch.tensor([1/3, 1/3, 1/3]))
print(x.grad)  # 约为 tensor([0.6667, 1.3333, 2.0000])
```

这里传入的是**到达 y 各元素的起始导数**，并非最终的 x.grad。还要经过平方节点，分别乘上 `2x`。在这个例子中，它与对 y 的均值反向得到相同结果。

## 8. autograd.grad：直接返回梯度

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2

(g,) = torch.autograd.grad(y, x)
print(g)       # tensor(4.)
print(x.grad)  # None
```

`torch.autograd.grad(y, x)` 表示求 y 对 x 的导数，并把结果返回。结果是元组，`(g,)` 取出其中唯一的一项。

**它也执行了反向计算，只是默认不把结果累加到输入的 `.grad`。** 因而不能看到 `x.grad is None`，就断定没有求过导。

| 方式 | 梯度结果放在哪里 |
| --- | --- |
| `y.backward()` | 通常累加到需要梯度的叶子张量的 `.grad` |
| `autograd.grad(y, x)` | 直接返回指定输入的梯度 |

## 9. create_graph：把求导过程也记录下来

假设 `y=x³`：一阶导数是 `3x²`，二阶导数是 `6x`。想继续对一阶导数求导，只知道它当前的数值还不够，还需要它如何依赖 x 的计算关系。

默认情况下：

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 3
(g,) = torch.autograd.grad(y, x)

print(g)                # tensor(12.)
print(g.requires_grad)  # False
```

反向确实计算了 `3*x**2`，但默认没有为这段求导运算建立新的求导关系。对这个 g 再求导就没有路径可走。

开启 `create_graph=True`：

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 3
(g,) = torch.autograd.grad(y, x, create_graph=True)

print(g)                # tensor(12., grad_fn=...)
print(g.requires_grad)  # True

(h,) = torch.autograd.grad(g, x)
print(h)                # tensor(12.)，因为 6x=12
```

```text
原来的前向图：
x ──立方──→ y

求一阶导数时记录的计算关系：
x ──平方──→ x² ──乘 3──→ g
                          │
                     再对 x 求导
                          ↓
                       h = 6x
```

两次得到的 g 都是 12，区别在于后者还记录着它对 x 的求导关系。一阶与二阶导数这次恰好数值相等，含义却不同：一个描述 y 怎样变，一个描述 y 的导数怎样变。

**retain_graph 保留“再算一次原导数”所需的信息；create_graph 记录“继续对导数求导”所需的关系。** 单独设置 retain_graph，并不能代替 create_graph。这里讨论的是继续对自动求导结果求导的做法，不是说所有二阶导数计算方法都必须使用这个参数。

## 10. 把几个开关放回各自的位置

| 概念或操作 | 解决的问题 |
| --- | --- |
| `requires_grad` | 张量是否需要梯度，并影响相关运算的记录 |
| `grad_fn` / `next_functions` | 观察反向节点与连接，不是梯度数值 |
| `backward()` | 启动反向计算，并累加梯度结果 |
| `.grad` / `retain_grad()` | 梯度结果保存在哪里，是否保留中间梯度 |
| `.grad = None` | 清掉已保存的梯度结果 |
| `no_grad()` | 范围内的普通计算不记录求导关系 |
| `detach()` | 从已有张量得到断开求导关系的张量 |
| `retain_graph=True` | 保留原图再次反向需要的信息 |
| `autograd.grad()` | 直接返回指定输入的梯度 |
| `create_graph=True` | 记录求导过程，支持继续对梯度求导 |

这些操作分别作用于记录、执行、保存等不同环节。把它们拆开理解，就不必靠记住几段固定代码来猜结果。

## 参考资料

本文只整理本节已经讨论过的内容。API 行为可核对 PyTorch 官方的 [Autograd mechanics](https://docs.pytorch.org/docs/stable/notes/autograd.html)、[Tensor.backward](https://docs.pytorch.org/docs/stable/generated/torch.Tensor.backward.html) 和 [torch.autograd.grad](https://docs.pytorch.org/docs/stable/generated/torch.autograd.grad.html)。

## 小结与自检

这一节的主线是：**前向记录关系，反向沿图计算，最后按所选方式保存或返回梯度。** 记录关系、执行计算和保存结果，是三件相关但不同的事。

1. `grad_fn` 已存在，能说明已经执行反向计算吗？**答：不能，它说明相应反向关系已经记录。**
2. u 参与了反向计算，为什么默认 `u.grad` 仍可能是 None？**答：非叶子张量默认不保留自己的梯度结果，需要时可提前调用 retain_grad。**
3. 保留原图后反向两次，x.grad 翻倍，是二阶导数吗？**答：不是，同一个一阶导数被计算两次并累加。**
4. 用 `no_grad` 算 u=x²，范围外算 v=3x，再对 y=u+v 反向，x=2 时梯度是多少？**答：3，经过 u 回到 x 的路径没有记录。**
5. `u=u.detach()` 删除了原图吗？**答：没有，它让变量名指向断开求导关系的张量，其他引用仍可保留原关系。**
6. create_graph 与 retain_graph 的核心区别是什么？**答：前者记录求导过程，让梯度也能继续被求导；后者保留原图再次反向所需的信息。**
