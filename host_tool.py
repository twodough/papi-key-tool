import base64
import json
import random

def generate_papi_game():
    print("🎭 怕屁遊戲主持人腳本 🎭")
    print("-" * 30)
    
    players = []
    while True:
        name = input("輸入玩家姓名 (或按 Enter 結束): ").strip()
        if not name:
            break
        pub_raw = input(f"貼上 {name} 的公鑰: ").strip()
        if pub_raw:
            players.append({"name": name, "pub_raw": pub_raw})
    
    if len(players) < 2:
        print("❌ 至少需要兩位玩家！")
        return

    # 隨機決定兇手
    killer_idx = random.randint(0, len(players) - 1)
    
    print("\n請執行以下步驟：")
    print("1. 下面這段程式碼會幫你產生加密訊息。")
    print("2. 因為 RSA 加密比較複雜，我建議妳直接使用我提供的『加密輔助函式』。")
    print("\n--- 加密結果 (請複製到群組) ---")
    
    # 這裡因為 Python 原生不帶 RSA-OAEP SHA-256，
    # 為了方便土豆小姐執行，我建議我們用一個簡單的「加密網頁」或是
    # 幫妳寫一個依賴 pycryptodome 的 Python 腳本。
    
    # 考慮到土豆小姐可能想要「純 Python」，我先假設環境已經有 pycryptodome：
    # pip install pycryptodome
    
    try:
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_OAEP
        from Crypto.Hash import SHA256

        output = "🎭 怕屁加密身分名單 🎭\n請複製自己的代碼到工具解密：\n\n"
        
        for i, p in enumerate(players):
            is_killer = (i == killer_idx)
            message = "你是兇手 😈" if is_killer else "你是無辜 😇"
            
            # 解析 JWK (網頁產生的格式)
            pub_data = json.loads(base64.b64decode(p['pub_raw']).decode())
            jwk = pub_data['k']
            
            # 簡化 JWK 轉 RSA (這裡我們主要需要 n 和 e)
            def b64_to_int(s):
                # Add padding
                s += '=' * (4 - len(s) % 4)
                return int.from_bytes(base64.urlsafe_b64decode(s), 'big')
            
            n = b64_to_int(jwk['n'])
            e = b64_to_int(jwk['e'])
            
            public_key = RSA.construct((n, e))
            cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
            encrypted = cipher.encrypt(message.encode('utf-8'))
            
            cipher_b64 = base64.b64encode(encrypted).decode()
            output += f"{p['name']}：\n{cipher_b64}\n\n"
            
        print(output)
        
    except ImportError:
        print("\n❌ 偵測到缺少套件！請先執行：")
        print("uv pip install pycryptodome")
        print("\n(因為網頁版是用 RSA-OAEP SHA-256，Python 端需要這個套件才能正確加密喔！)")

if __name__ == "__main__":
    generate_papi_game()
