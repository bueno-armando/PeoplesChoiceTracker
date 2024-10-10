import requests
import os
from bs4 import BeautifulSoup   

# METHOD: get likes from an instagram post
def get_ig_likes(post_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(post_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the likes count (this may vary based on Instagram's HTML structure)
    likes = soup.find('meta', property='og:description')['content']
    
    # Extract the likes count from the description
    if likes:
        # Remove commas and convert to integer
        likes_count = likes.split(' ')[0].replace(',', '')  # Remove commas
        return int(likes_count)  # Convert to integer
    else:
        return 0  # Return 0 if likes count not found

# METHOD: get reactions from a facebook photo
def get_fb_reactions(photo_id):
    access_token = os.getenv('FB_TOKEN')
    url = f"https://graph.facebook.com/v18.0/{photo_id}?fields=likes.summary(true)&access_token={access_token}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if 'likes' in data:
            total_likes = data['likes']['summary']['total_count']
            return int(total_likes)  # Ensure this is an integer
        elif 'error' in data:
            return 0  # Return 0 if there's an error
        else:
            return 0  # Return 0 if like data not found in the response.
    
    except requests.exceptions.HTTPError as http_err:
        return 0  # Return 0 on HTTP error
    except requests.exceptions.RequestException as req_err:
        return 0  # Return 0 on request error
    except Exception as e:
        return 0  # Return 0 on unexpected error

# CLASS: social media posts for teams (with both ig and fb links)
class SocialMediaPost:
    def __init__(self, team, facebook_id, instagram_url):
        self.team = team
        self.facebook_id = facebook_id
        self.instagram_url = instagram_url

    @property
    def facebook_url(self):
        return f"https://www.facebook.com/photo.php?fbid={self.facebook_id}"

# OBJECT DEFINITIONS (teams with both fb and ig links)
social_media_posts = [
    SocialMediaPost('Agrosky', '1051036087026243', 'https://www.instagram.com/p/DA1zqUOgXi_/'),
    SocialMediaPost('Aventureros', '1051036107026241', 'https://www.instagram.com/p/DA1zrB4Avru/'),
    SocialMediaPost('Derat to the Stars', '1051036100359575', 'https://www.instagram.com/p/DA1zmpUAEqp/'),
    SocialMediaPost('Dinos', '1051036173692901', 'https://www.instagram.com/p/DA1z9LTgp9r/'),
    SocialMediaPost('Galactic Snack', '1051036200359565', 'https://www.instagram.com/p/DA1zqYQA3C6/'),
    SocialMediaPost('Gomitas Galacticas', '1051036210359564', 'https://www.instagram.com/p/DA10NakgJYG/'),
    SocialMediaPost('Home Officers', '1051036260359559', 'https://www.instagram.com/p/DA10IwEAYtV/'),
    SocialMediaPost('Intolerantes al JS', '1051036323692886', 'https://www.instagram.com/p/DA10Mp_AYmr/'),
    SocialMediaPost('Iseljas', '1051036340359551', 'https://www.instagram.com/p/DA10O_AgGHW/'),
    SocialMediaPost('M.A.V.I.S.E', '1051036360359549', 'https://www.instagram.com/p/DA10JMbAAK2/'),
    SocialMediaPost('M-CUU', '1051036423692876', 'https://www.instagram.com/p/DA10NMhAz9S/'),
    SocialMediaPost('MoonLaders', '1051036430359542', 'https://www.instagram.com/p/DA10LqwgnMy/'),
    SocialMediaPost('nWorks', '1051036453692873', 'https://www.instagram.com/p/DA10OyxA1Qs/'),
    SocialMediaPost('ODD', '1051036507026201', 'https://www.instagram.com/p/DA10K_xARw7/'),
    SocialMediaPost('Per Oceanis Procellas', '1051036547026197', 'https://www.instagram.com/p/DA10OaTAf9t/'),
    SocialMediaPost('Polaris', '1051036570359528', 'https://www.instagram.com/p/DA10vckgtV4/'),
    SocialMediaPost('Prometheans', '1051036587026193', 'https://www.instagram.com/p/DA10OMoAFpm/'),
    SocialMediaPost('RedStoners', '1051036627026189', 'https://www.instagram.com/p/DA10QQuAKca/'),
    SocialMediaPost('Sirio Estelar', '1051036670359518', 'https://www.instagram.com/p/DA10SgKAJtE/'),
    SocialMediaPost('Space Bytes', '1051036680359517', 'https://www.instagram.com/p/DA10VOMAHnf/'),
    SocialMediaPost('Spider', '1051036720359513', 'https://www.instagram.com/p/DA10YZbAOau/'),
    SocialMediaPost('Supernova Family', '1051036747026177', 'https://www.instagram.com/p/DA10ahagw99/'),
    SocialMediaPost('Syntax Error', '1051036787026173', 'https://www.instagram.com/p/DA10cr1gvBa/'),
    SocialMediaPost('Team Estelas', '1051036810359504', 'https://www.instagram.com/p/DA10emYAtyY/'),
    SocialMediaPost('The CMDers', '1051036833692835', 'https://www.instagram.com/p/DA10gvugwvo/'),
    SocialMediaPost('Wave Inn', '1051036877026164', 'https://www.instagram.com/p/DA10iusA3Py/'),
    SocialMediaPost('Where is Alpha?', '1051036900359495', 'https://www.instagram.com/p/DA10kc6gtBT/'),
]

# List to store results
results = []

# Update the loop to fetch likes for both platforms and calculate total reactions
for post in social_media_posts:
    fb_reactions = get_fb_reactions(post.facebook_id)
    ig_likes = get_ig_likes(post.instagram_url)
    
    # Calculate total reactions
    total_reactions = fb_reactions + ig_likes
    
    # Append results to the list
    results.append({
        'team': post.team,
        'fb_reactions': fb_reactions,
        'ig_likes': ig_likes,
        'total_reactions': total_reactions
    })

# Sort results by total reactions in descending order
sorted_results = sorted(results, key=lambda x: x['total_reactions'], reverse=True)

# Print header
print(f"{'Team':<25} {'FB':<15} {'IG':<15} {'Total':<15}")
print('-' * 70)  # Separator line

# Print sorted results in a single line
for result in sorted_results:
    print(f"{result['team']:<25} {result['fb_reactions']:<15} {result['ig_likes']:<15} {result['total_reactions']:<15}")