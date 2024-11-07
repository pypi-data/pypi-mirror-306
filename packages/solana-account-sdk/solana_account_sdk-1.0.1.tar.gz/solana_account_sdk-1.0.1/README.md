### 功能： 此SDK用于生成solana助记词，并且通过助记词格式化私钥



### 1.安装

```
pip install solana-account-sdk
```

### 2. 导入

```
from solana_account_sdk.api import create_account, format_mnemonic
```

### 3. 基本使用

- 创建新的账户

  ```
  new_account = create_account()
  print(new_account)
  ```

- 通过助记词格式化账户信息

  ```
  words = 'change build leaf until climb assault ignore sand have arrow bless jaguar'
  format_account = format_mnemonic(words)
  print(format_account)
  ```

### 4.参数说明

- ```
  create_account方法参数说明
  _mnemonic_words  >>  助记词长度, (12或24), 默认为12
  _dpath	>> 派生路径 例如 < phantom钱包的默认派生路径为: m/44'/501'/0'/0' >, 默认为空
  _debug  >> 是否打印账户账户信息, 默认False, 不打印
  ```

