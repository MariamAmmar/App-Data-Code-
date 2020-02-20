#!/usr/bin/env python
# coding: utf-8

# **In-App User Advertistment Views**
# 
# The goal of this project is to help developers understand which types of apps are more likely to attract viewers in order to maximize profit recieved from in-app ads. 

# In[1]:


from csv import reader

### The Google Play data set ###
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

### The App Store data set ###
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# In[2]:



def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line between rows
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

print(android_header)
print('\n')
explore_data(android, 0, 3, True)


# In[3]:


print(ios_header)
print('\n')
explore_data(ios, 0, 3, True)


# In[4]:


for app in android:
    name=app[0]
    if name =='Instagram':
        print(app)


# The Google Play data set has duplicate entries such as those pictured above. The entries will not be removed randomly. The rows with the highest number of reviews will be kept. 

# In[5]:


duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)

print('Number of duplicate apps:',len(duplicate_apps))
print('\n')
print('Examples of duplicate apps', duplicate_apps[:15])



# In[6]:


print(android[10472])


# In[7]:


del (android[10472])
print(android[10472])


# In[8]:


print('Expected length:',len(android)-1181)#This last number is the number of duplicates. 


# In[9]:


reviews_max = {}

for app in android[1:]:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews

print(len(reviews_max))


# The reviews_max dictionary will be used to remove duplicates. 

# In[10]:


already_added = []
android_clean = []

for app in android[1:]:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# Next, a function is written in order to remove all non-English text from the data since the purpose of this project is to target information related to English-speaking app viewers.  

# In[11]:


def isitEnglish(string):
    non_ascii = 0
    for character in string:
        if ord(character)>127:
            non_ascii+=1
    
    if non_ascii>3:
        return False
    else:
        return True

print(isitEnglish('Instagram'))
print(isitEnglish('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(isitEnglish('Docs To Go™ Free Office Suite'))
print(isitEnglish('Instachat 😜'))


# Since this function defines string names that have emojis or other types of characters as non-English, this will lose reliable data inputs, so a new function is created in order to allow these inputs to remain by only excluding entries that have more than 3 characters that fall outside of our "English" scope. 

# In[12]:


android_english=[]
ios_english=[]

for app in android_clean:
    name=app[0]
    if isitEnglish(name):
        android_english.append(app)

for app in ios:
    name=app[0]
    if isitEnglish(name):
        ios_english.append(app)

explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# The following command will loop through the datasets and remove apps that are not free since the main source of revenue consists of in-app ads. 

# In[13]:


android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)
        
print(len(android_final))
print(len(ios_final))


# Next it is crucial to find an app profile that fits both the App Store and Google Play. To minimize risks and overhead, the validation strategy for an app idea is comprised of three steps:
# 
# 1. Build a minimal Android version of the app, and add it to Google Play.
# 
# 2. If the app has a good response from users, it will be developed further.
# 
# 3. If the app is profitable after six months, an iOS version of the app will be built and added to the App Store.

# In[14]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1

    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    return table_percentages
    
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])

print('iOS Genres')
display_table(ios_final, -5)
print('\n')
print('Android Categories')
display_table(android_final,1)
print('\n')
print('Android Genres')
display_table(android_final, -4)


# In[15]:


genre_ios=freq_table(ios_final,-5)

for genre in genre_ios:
    total=0
    len_genre=0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    average_nratings = total/len_genre 
    print(genre,':',average_nratings)


# In[22]:


android_category = freq_table(android_final,1)

for category in android_category:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs = n_installs.replace('+','')
            n_installs = n_installs.replace(',','')
            total += float(n_installs)
            len_category +=1
    average_n_installs = total/len_category
    print(category,':',average_n_installs)
   

        

