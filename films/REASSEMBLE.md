# 分卷重组说明

6 个 >100MB 的战役归档 tar 已按 95MB 分卷存储（`split -b 95M -d`）。

重组方法（任一系统）：
```
cat P50_B.tar.part-00 P50_B.tar.part-01 P50_B.tar.part-02 P50_B.tar.part-03 P50_B.tar.part-04 > P50_B.tar
```
（其余同理：按 part-00..N 顺序 cat 拼接）

校验：原始 tar 与分卷的 SHA256 见 `manifests/sha256-index.csv`；
原始包内容=对应战役的完整项目运行现场（input/output/过程记录）。
