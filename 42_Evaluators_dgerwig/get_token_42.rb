require "oauth2"

UID = "afb6d14d4e14215ec14e0ce9ca8fe7378dae8ee98dc9563094f158f137f65bf0"
SECRET = "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"

# Create the client with your credentials
client = OAuth2::Client.new(UID, SECRET, site: "https://api.intra.42.fr")

# Get an access token
token = client.client_credentials.get_token

# Print the token
puts "Access Token: #{token.token}"

sleep(1)

page_number = 1
all_user_info = []

loop do
  begin
    campus_users_response = token.get("/v2/campus/40/users", params: { page: { number: page_number } }).parsed

    if campus_users_response.is_a?(Array) && !campus_users_response.empty?
      user_info = campus_users_response.select { |user| !user["staff?"] && user["active?"] && user["pool_year"] == "2021"}
                                      .map { |user| { "login" => user["login"], "id" => user["id"] } }
      all_user_info.concat(user_info)
  
      puts "💥 Users info: #{user_info}"
    else
      puts "❗ Wrong format or empty list."
      break
    end

    page_number += 1
  rescue => e
    puts "❌ Error! #{e.message}"
    break  
  end
end

puts "\n✅ Users info: #{all_user_info}"
puts "\n✅ Number of users: #{all_user_info.count}"

all_user_info.each do |user|
    users_info = token.get("/v2/users/#{user['id']}").parsed
    cursus_users_info = users_info['cursus_users']

    sleep(0.5)
    cursus_users_info.each do |cursus_user|
        if cursus_user['cursus']['slug'] == '42cursus'
            user['cursus_level'] = cursus_user['level']
        end
    end
end

puts "\n✅ Updated Users info: #{all_user_info}"

sorted_user_info = all_user_info.sort_by { |user| -user['cursus_level'].to_f }

puts "\n✅ Sorted Users info (Highest to Lowest Level):"
sorted_user_info.each do |user|
    puts "User: #{user['login']} - Level: #{user['cursus_level']}"
end


require 'csv'
require 'time'

current_time = Time.now.strftime("%Y%m%d_%H%M%S")

csv_filename = "42_users_ranking_#{current_time}.csv"

# sorted_user_info = all_user_info.sort_by { |user| -user['cursus_level'].to_f }

CSV.open(csv_filename, 'wb') do |csv|
    csv << ['User', 'Cursus Level']

    sorted_user_info.each do |user|
        csv << [user['login'], user['cursus_level']]
    end
end

puts "\n✅ CSV file '#{csv_filename}' has been created."