


# 1 填充自己的私钥
privateKey = ''


# 2.跨链金额（goerli测试网）
bridge_eth = 0.005

# 3.官方合约跨链
hash = ScrolBirdgeGoerliToScrol(goerli_w3,privateKey,bridge_eth)
print(f"跨链成功 hash:{hash}")


