import json
import getpass
from wikidataintegrator import wdi_core, wdi_login

def main():
    print("=== ADICIONAR TERMOS A PARTIR DE JSON ===")
    user = input("Nome de utilizador do bot (ex: Utilizador@bot): ").strip()
    password = getpass.getpass("Senha do bot: ").strip()
    
    try:
        login = wdi_login.WDLogin(user=user, pwd=password)
        print("✅ Autenticado com sucesso!\n")
    except Exception as e:
        print(f"❌ Falha na autenticação: {e}")
        return

    arquivo = input("Caminho do ficheiro JSON (ex: termos_teste.json): ").strip()
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados_json = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler o JSON: {e}")
        return

    item_id = dados_json.get("item_id")
    lang = dados_json.get("lang", "pt")
    label = dados_json.get("label", "")
    desc = dados_json.get("description", "")
    aliases = dados_json.get("aliases", [])

    if not item_id or not item_id.startswith("Q"):
        print("❌ O JSON precisa de um 'item_id' válido (ex: Q42).")
        return

    termos = []
    if label:
        termos.append(wdi_core.WDString(value=label, prop_type="label", lang=lang))
    if desc:
        termos.append(wdi_core.WDString(value=desc, prop_type="description", lang=lang))
    for alias in aliases:
        termos.append(wdi_core.WDString(value=alias, prop_type="alias", lang=lang))

    if not termos:
        print("Nenhum termo encontrado no JSON.")
        return

    try:
        item = wdi_core.WDItemEngine(wd_item_id=item_id)
        item.write(termos, login=login, edit_summary="Adicionar termos via JSON")
        print(f"✅ Termos adicionados ao item {item_id}!")
    except Exception as e:
        print(f"❌ Erro ao gravar: {e}")

if __name__ == "__main__":
    main()
