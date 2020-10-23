# TensorTime

[![Pypi](https://img.shields.io/pypi/v/tensortime.svg)](https://pypi.org/project/tensortime/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/dovolopor-research/tensortime/blob/main/LICENSE)
[![stars](https://img.shields.io/github/stars/dovolopor-research/tensortime.svg)](https://github.com/dovolopor-research/tensortime/stargazers)

🕙 **TensorTime 让你的实验可以回溯！**

## 1 缘起

在训练模型时，可能有很多参数需要调试，有时我们会把结果和参数记录下来。
由于代码和数据等各种细节都可能会改变，所以在回溯代码时，就可能会发生无法复现先前结果的状况。

版本控制工具是一个解决的办法，但是 git 管理起大文件不是特别方便。
所以我们需要一个工具既可以保存代码这种小文件，也要能保存数据和模型这种大文件。

`TensorTime` 就是这样一个工具，它在每次运行实验时，完整的复制一份代码和数据到特定的文件夹里。
任何时候你都可以重新回溯，复现出先前的实验！

当然这样做也有一个很大的缺点，就是比较占用空间，因此 TensorTime 可以选择性的忽略一些文件或文件夹。
比如有些实验的数据集就是不会变动的，可以选择直接忽略掉。

总的来说，TensorTime 是一种 **「空间换时间」** 的做法，希望你用得愉快～

## 2 安装

```bash
# 使用 pip 安装
pip install tensortime

# 从代码库安装
git clone https://github.com/dovolopor-research/tensortime.git
cd tensortime && python setup.py install
```

## 3 快速上手

### 3.1 引入

```python
# 通常在 train.py 文件下
from tensortime import TimeMachine
# ....
if __name__ == "__main__":
    tm = TimeMachine()
    tm.backup()
    # ...
```

### 3.2 执行

```bash
# 正常执行文件，在开始运行时会要求输入实验备注
python train.py

>> tensortime: 输入实验备注 nlp
>> tensortime: 创建备份文件夹 tensortime
>> tensortime: 创建实验文件夹 Fri_Oct_23_09:36:04_2020-nlp
>> tensortime: 忽略 model
>> tensortime: 备份 train.py
>> tensortime: 忽略 tensortime
>> tensortime: 备份 .git
>> tensortime: 忽略 test.sh
>> tensortime: 备份 .ttignore
>> tensortime: 成功备份到 tensortime/Fri_Oct_23_09:36:04_2020-nlp
```

在 `tensortime/Fri_Oct_23_09:36:04_2020-nlp` 下即可找到本次实验的所有文件。

### 3.3 忽略

从上文的日志中可以看到，有些文件是不希望备份进去的，比如 `temp.py`、`.git`。

我们可以直接在 backup 里设置参数，忽略掉指定文件。

```python
tm.backup(ignore=["temp.py", ".git"])
```

另外还可以使用类似于 `.gitignore` 的方式，在项目的主目录下创建一个 `.ttignore`。

```gitignore
# .ttignore
# 忽略文件（以#开头的是注释，不会被解析）
temp.py

# 忽略文件夹
.git/
```

> 注：暂时不支持一级以上的忽略，比如 `model/cnlp.py`。

### 3.4 附加

前面的代码展示了如何忽略不需要的文件，这个操作一般是在所有代码运行前。

对于深度学习应用来说，我们有一项非常重要的数据——权重，它一般是代码跑完后才会生成的。

因此我们需要在保存权重后，再执行一遍备份操作，这个时候仅仅需要备份权重文件。

```python
tm.backup(add=["save"])
```

## 4 进阶

### 4.1 自定义 TimeMachine 参数

- backup_dir: 指定备份文件夹，默认为 tensortime
- exp_dir: 指定实验文件夹，默认为 时间 + 备注
- exp_suffix: 指定实验文件夹的备注（在 exp_dir 为 None 时生效）

## 5 许可

[![](https://award.dovolopor.com?lt=License&rt=MIT&rbc=green)](./LICENSE)
