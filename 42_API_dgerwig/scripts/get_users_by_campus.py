import requests
from get_token_42 import get_access_token

def get_users_by_campus(access_token, campus_id):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    page_number = 1
    all_user_info = []

    while True:
        try:
            response = requests.get(f"https://api.intra.42.fr/v2/campus/{campus_id}/users", headers=headers, params={
                'page[number]': page_number
            })
            response.raise_for_status()
            campus_users_response = response.json()

            if isinstance(campus_users_response, list) and campus_users_response:
                user_info = [
                    {'login': user['login'], 'id': user['id']}
                    for user in campus_users_response
                    # if not user.get('staff?') and (user.get('pool_year') == '2021' or user.get('pool_year') == '2022')
                    # if not user.get('staff?') and user.get('active?') and user.get('pool_year') == '2021'
                    # if not user.get('staff?') and user.get('active?') and (user.get('pool_year') == '2021' or user.get('pool_year') == '2022')
                    if not user.get('staff?') and user.get('pool_year') == '2021' and user.get('pool_month') == 'april'
                ]
                all_user_info.extend(user_info)
                print(f"💥 {page_number}\tUsers info: {user_info}")
            else:
                print("❗ Wrong format or empty list.")
                break

            page_number += 1
        except Exception as e:
            print(f"❌ Error! {e}")
            break
    
    return all_user_info

if __name__ == "__main__":
    access_token = get_access_token()
    print(f"✨ Access Token: {access_token}")
    campus_id = 40  
    users = get_users_by_campus(access_token, campus_id)
    with open('all_users.json', 'w') as f:
        import json
        json.dump(users, f)
    print("✅ Users fetched and saved to all_users.json")
