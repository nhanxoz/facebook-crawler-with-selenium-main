import requests

def get_final_image_url(redirect_url):
    response = requests.get(redirect_url, allow_redirects=True)
    final_image_url = response.url
    return final_image_url

redirect_url = "https://m.facebook.com/photo/view_full_size/?fbid=646123469471928&ref_component=mbasic_photo_permalink&ref_page=%2Fwap%2Fphoto.php&refid=13&__tn__=%2Cg"
final_image_url = get_final_image_url(redirect_url)
print("Final Image URL:", final_image_url)