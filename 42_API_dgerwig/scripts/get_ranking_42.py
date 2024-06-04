import requests
import time
import csv
from datetime import datetime
import os
from tqdm import tqdm
from get_token_42 import get_access_token


def get_user_data(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    page_number = 1
    all_user_info = []

    while True:
        try:
            response = requests.get(f"https://api.intra.42.fr/v2/campus/40/users", headers=headers, params={
                'page[number]': page_number
            })
            response.raise_for_status()
            campus_users_response = response.json()

            if isinstance(campus_users_response, list) and campus_users_response:
                user_info = [
                    {'login': user['login'], 'id': user['id']}
                    for user in campus_users_response
                    if not user.get('staff?') and user.get('active?') and user.get('pool_year') == '2021'
                ]
                all_user_info.extend(user_info)

                print(f"💥 Users info: {user_info}")
            else:
                print("❗ Wrong format or empty list.")
                break

            page_number += 1
        except Exception as e:
            print(f"❌ Error! {e}")
            break

    print(f"\n✅ Users info: {all_user_info}")
    print(f"\n✅ Number of users: {len(all_user_info)}")

    progress_bar = tqdm(all_user_info, desc="Fetching user data", unit="user")

    for user in all_user_info:
        user_response = requests.get(f"https://api.intra.42.fr/v2/users/{user['id']}", headers=headers)
        user_response.raise_for_status()
        users_info = user_response.json()
        cursus_users_info = users_info['cursus_users']

        time.sleep(0.5)
        for cursus_user in cursus_users_info:
            if cursus_user['cursus']['slug'] == '42cursus':
                user['cursus_level'] = cursus_user['level']

        progress_bar.set_postfix({'Cursus Level': user.get('cursus_level', 'N/A')})

    progress_bar.close()

    print(f"\n✅ Updated Users info: {all_user_info}")

    sorted_user_info = sorted(all_user_info, key=lambda user: -float(user.get('cursus_level', 0)))

    print("\n✅ Sorted Users info (Highest to Lowest Level):")
    for user in sorted_user_info:
        print(f"User: {user['login']} - Level: {user.get('cursus_level')}")

    data_folder = "data"
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"42_users_ranking_{current_time}.csv"
    csv_path = os.path.join(data_folder, csv_filename)
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['User', 'Cursus Level'])

        for user in sorted_user_info:
            csvwriter.writerow([user['login'], user.get('cursus_level')])

    print(f"\n✅ CSV file '{csv_filename}' has been created.")


if __name__ == "__main__":
    access_token = get_access_token()
    print(f"✨ Access Token: {access_token}")
    get_user_data(access_token)
