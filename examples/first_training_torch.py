"""第一课可选 PyTorch 实验。仅需 CPU；先安装适合自己环境的 torch。"""
import torch


def run():
    x = torch.tensor([[0.0], [1.0], [2.0]])  # [batch=3, features=1]
    y = torch.tensor([[1.0], [3.0], [5.0]])  # [3, 1]
    model = torch.nn.Linear(1, 1)
    with torch.no_grad():
        model.weight.zero_()
        model.bias.zero_()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    for _ in range(100):
        optimizer.zero_grad()              # 清除上一步累积的梯度
        pred = model(x)                     # [3, 1]
        loss = ((pred - y) ** 2).mean() / 2 # 与手算完全一致
        loss.backward()                    # 计算梯度，不更新参数
        optimizer.step()                   # 使用梯度更新参数
    with torch.no_grad():
        final_loss = ((model(x) - y) ** 2).mean() / 2
    print(f'w={model.weight.item():.6f}, b={model.bias.item():.6f}, loss={final_loss.item():.8f}')
    return model, final_loss.item()


if __name__ == '__main__':
    run()
