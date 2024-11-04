# mcp_persor
mocopiで作成したBVHファイルを解析するパッケージです。

# インストール
```bash
pip install git+https://github.com/SatooRu65536/mcp_persor.git

or

pip install mcp-persor
```

# 使い方
## インポート
```python
from mcp_persor import BVHparser
```

## ファイルを読み込む
```python
bvhp = BVHparser('path/to/bvh/file')
```

## Dataframe として取得する
```python
motion_df = bvhp.get_motion_df()
```

# LICENSE
[MIT](./LICENSE)
