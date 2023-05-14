from geopy.geocoders import Nominatim

loc = Nominatim(user_agent="test1")

getlocation = loc.geocode("三ノ宮駅")

print("住所: ",getlocation.address,"\n")
print("緯度: ",getlocation.latitude,"\n")
print("経度: ",getlocation.longitude,"\n")
print("詳細な情報: ",getlocation.raw)