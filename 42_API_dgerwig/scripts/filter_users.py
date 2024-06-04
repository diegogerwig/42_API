import json

def filter_users(users, year, month):
    filtered_users = [
        user for user in users
        if not user.get('staff?') and user.get('pool_year') == year and user.get('pool_month') == month
    ]
    return filtered_users

if __name__ == "__main__":
    with open('all_users.json', 'r') as f:
        users = json.load(f)
    
    year = '2021'  
    month = 'april'  
    filtered_users = filter_users(users, year, month)
    
    with open('filtered_users.json', 'w') as f:
        json.dump(filtered_users, f)
    
    print("✅ Users filtered and saved to filtered_users.json")