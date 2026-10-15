"""第一课：纯 Python 全批量梯度下降，无第三方依赖。"""
import argparse
import json

DATA = [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0)]


def loss_and_grad(w, b, data=DATA):
    """L = mean((w*x+b-y)^2)/2；返回 loss, dL/dw, dL/db。"""
    n = len(data)
    errors = [(x, w * x + b - y) for x, y in data]
    return (sum(e * e for x, e in errors) / (2 * n),
            sum(e * x for x, e in errors) / n,
            sum(e for x, e in errors) / n)


def step(w, b, lr, data=DATA):
    _, dw, db = loss_and_grad(w, b, data)
    # 两个梯度均来自更新前的同一组参数。
    return w - lr * dw, b - lr * db


def train(lr=0.1, steps=100):
    w, b = 0.0, 0.0
    history = []
    for i in range(steps + 1):
        loss, dw, db = loss_and_grad(w, b)
        history.append(dict(step=i, w=w, b=b, loss=loss, dw=dw, db=db))
        if i < steps:
            w, b = step(w, b, lr)
    return history


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lr', type=float, default=0.1)
    parser.add_argument('--steps', type=int, default=100)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if args.steps < 0 or args.steps > 10000:
        parser.error('--steps must be between 0 and 10000')
    history = train(args.lr, args.steps)
    if args.json:
        print(json.dumps(history))
    else:
        print('step       w        b        loss')
        for row in history:
            if row['step'] in {0, 1, 2, 10, args.steps}:
                print(f"{row['step']:4d} {row['w']:8.4f} {row['b']:8.4f} {row['loss']:11.6f}")
