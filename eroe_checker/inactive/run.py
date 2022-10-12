from math import sqrt
import json
old = {}
new = {}
new2 = {}



with open("map3.sql") as fp:
    Lines = fp.readlines()
    for line in Lines:
        l = line[30:-3].split(",")
        try:
            old[l[0]] = {
                "x":int(l[1]), "y":int(l[2]), "pop":int(l[10])
            }
        except:
            continue


with open("map4.sql") as fp:
    Lines = fp.readlines()
    for line in Lines:
        l = line[30:-3].split(",")
        try:
            new[l[0]] = {
                "x":int(l[1]), "y":int(l[2]), "pop":int(l[10])
            }
        except:
            continue

with open("map6.sql") as fp:
    Lines = fp.readlines()
    for line in Lines:
        l = line[30:-3].split(",")
        try:
            new2[l[0]] = {
                "x":int(l[1]), "y":int(l[2]), "pop":int(l[10])
            }
        except:
            continue


print(len(new),len(old))

X=69
Y=30

count = 0
inattivi = []
for k in old:
    info_old = old[k]
    distance = sqrt( (info_old["x"]-X)**2 + (info_old["y"]-Y)**2 )

    if distance > 100 or info_old["pop"] < 110:
        continue
    
    if k not in new or k not in new2:
        continue

    info_new = new[k]
    info_new2 = new2[k]


    if info_new["pop"] == info_old["pop"] == info_new2["pop"]:
        info_new["distance"] = distance
        inattivi.append(info_new)
        count += 1
    

print(count)

inattivi2 = sorted(inattivi, key=lambda d: d['distance']) 
print(inattivi2)


file1 = open('inattivi_high.txt', 'w+')

for x in inattivi2:
    file1.write(json.dumps(x))
    file1.write("\n")
  
# Closing file
file1.close()


