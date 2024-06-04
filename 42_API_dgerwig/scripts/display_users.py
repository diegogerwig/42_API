import requests
import time
import csv
from datetime import datetime
import os
from tqdm import tqdm
import json
from get_token_42 import get_access_token

def fetch_detailed_user_info(access_token, user):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    user_response = requests.get(f"https://api.intra.42.fr/v2/users/{user['id']}", headers=headers)
    user_response.raise_for_status()
    users_info = user_response.json()
    cursus_users_info = users_info['cursus_users']

    for cursus_user in cursus_users_info:
        if cursus_user['cursus']['slug'] == '42cursus' and cursus_user['grade'] == 'Member' and cursus_user['level'] != 0:
            user['cursus_level'] = cursus_user['level']
            return user

    return user

def print_and_save_users(access_token, users):
    progress_bar = tqdm(users, desc="Fetching user data", unit="user")
    detailed_users_info = []

    for user in users:
        time.sleep(0.6)
        user = fetch_detailed_user_info(access_token, user)
        detailed_users_info.append(user)
        progress_bar.update()
        formatted_level = f"{user.get('cursus_level', 0.0):.2f}"
        if float(user.get('cursus_level', 0)) < 10:
            formatted_level = f"{formatted_level} "
        progress_bar.set_postfix({'Cursus Level': formatted_level})
    progress_bar.close()

    sorted_user_info = sorted(detailed_users_info, key=lambda user: -float(user.get('cursus_level', 0)))

    print("\n✅ Sorted Users info (Highest to Lowest Level):")
    for user in sorted_user_info:
        cursus_level = user.get('cursus_level', 0.0)
        try:
            formatted_level = f"{float(cursus_level):.2f}"
            if cursus_level < 10:
                formatted_level = f"{formatted_level} "  # Añadir espacio si es de un solo dígito
        except ValueError:
            formatted_level = user.get('cursus_level', 'N/A')

        print(f"User: {user['login']} \t- Level: {formatted_level}")

    data_folder = '/app/data'
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"42_users_ranking_{current_time}.csv"
    csv_path = os.path.join(data_folder, csv_filename)
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['User', 'Cursus Level'])

        for user in sorted_user_info:
            try:
                formatted_level = f"{user.get('cursus_level') or 'N/A':.2f}"
                if float(user.get('cursus_level', 0)) < 10:
                    formatted_level = f"{formatted_level} "  # Añadir espacio si es de un solo dígito
                csvwriter.writerow([user['login'], formatted_level])
            except ValueError:
                pass

    print(f"\n✅ CSV file '{csv_filename}' has been created.")

if __name__ == "__main__":
    access_token = get_access_token()
    with open('filtered_users.json', 'r') as f:
        users = json.load(f)
    
    print_and_save_users(access_token, users)