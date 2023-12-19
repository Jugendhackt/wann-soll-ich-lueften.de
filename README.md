# News
## Updated 30.10.23

## Post 19.12.23:
Reading time: about 5 minutes

Hello!

After another long time, I would like to say something about wann-soll-ich-lüften.de. I decided to completely reprogram wann-soll-ich-lüften.de with a friend. The reason for this is that it is very difficult to add new features to the software. When we started the project at JugendHackt 2022 in Cologne, we implemented everything in a very “improvised” way. Everything is quite confusing and I sometimes don't know where anything is anymore. That will change now. We have already started and will continue working on it in the next few days/weeks/months. We plan that the old version will also be available as a “legacy version”. I also have plans to develop a kit so that people who want to build an air measuring station can also be included in the wann-soll-ich-lüften.de system. That would also require a lot of resources and planning to implement such a system in addition to the API from where we get our data.

Wann-soll-ich-lüften.de also turned 1 year old in November!

I never thought the project would continue for so long. 1 year is such a long time, but it still went by quickly. I can still clearly remember where we programmed it together at the event. It was such a lovely time!

We will continue to keep you updated.
Merry Christmas and a Happy New Year!

Thanks!
Luis Schuimer

Velbert, Neviges on 12/19/23


## Post 08.08.23:
Reading time: about 5 minutes

Hello to our 4th post!
After a long time I have something to announce. In the last few days I've been looking at how to program a simple login system and am familiarizing myself with it. I don't WANT to do anything wrong like leaking user data because the code isn't secure. The whole topic is very important to me. I am now also registered for JugendHackt 2023 and will be there again. I don't know yet what I will do there, but I will try to program the website (wann-soll-ich-lüften.de) as a project at JugendHackt. Let's see. As you may know, we couldn't upload the newest version (2.5.5) to the server, because we had some problems. That's why I want to release "Stable" and "Experimental" versions now. These are then marked in the Updates tab. The "Experimental" version means that it is not a stable running version and errors can occur. The "Stable" version means that little to no errors can occur. We will always upload the "stable" versions to the server, and you can start the "experimental" versions on your PC and try them out on localhost. I'll soon be marking all the previous versions as well. In any case, the 2.5.5 version is currently "Experimental" and we will continue to program it soon and hopefully bring it to "Stable".

Thank you for reading!

Luis Schuimer
8/8/23
Velbert, North Rhine-Westphalia, Germany

## Post 28.02.23:

Hello to our 3rd post after we presented our goals for 2023. But today I have something new to share. We would like to prepare you for the 3.0 update. There will be one of the biggest changes we've ever made. accounts! Yes, you can create accounts and log in from the 3.0 update. You can set cities as your favorites and you can get all the data quickly. We will also look for some other API's for the data and then use them. However, this turns out to be difficult because a number of a station must be specified In the most API's. There is also another problem: We need storage space on our servers to store all login data. Currently we have 25GB of Storage. But there i still don't know how big data for 1 Account is but I will do some calculations here. But that costs money. More than I would like to pay alone. We don't know yet if you can look at voluntary advertising to support us or if you can donate. We definitely do NOT want to ask for money for a pro account with us or release data until you pay. So no worries there. 

Thank you for reading the post.

Luis Schuimer

## Post 1.1.23:

Hello everyone!
I would now like to announce what will change in 2023.
First, I might start up the old servers again for wann-soll-ich-lüften.de. The following new features are planned for later in the year!
- A JSON API that is easy to use thanks to simple and clear documentation
     - With this you can easily access our data
        which include our scale and other functions
- An hourly air quality forecast by an AI
- A notification via email or perhaps SMS when the
   air quality meets the specified condition.

More tests:
- A window that opens automatically
     -This should work together with wann-soll-ich-lüften.de

There may be other features that are not on the list.

Thanks!
Luis Schuimer

## Post 18.12.22:

Hello everyone!
a few days have passed without wann-soll-ich-lüften.de and there is news again. After some writing around in the JugendHackt community, the website was brought back online by some mentors (Philip, Ties and Jonas). Me and everyone else on the wann-soll-ich-lüften team say thank you to the mentors. Without you, the website would be offline for several months. Many thanks again to Jonas who owns the server and now hosts the website.

Thanks!
Luis Schuimer

# How to run the server
1. Download the preffered Version and unpack it
2. Make sure that you have Python installed.
3. Install the following Packages:
   Install them via pip install ...
        1. json
        2. requests
        3. prettytable
        4. flask

5. Run the server with the command: python3 server.py
6. Wait for the server to start (you need a internet connection for this)
7. Go on the URL you see in the console: http://127.0.0.1:5000

# wann-soll-ich-lueften.de
WebApp suggesting the best time to vent your apartment

https://www.youtube.com/watch?v=LCms1Pzf78Y

In what situations should I ventilate? This question is often asked. We have the answer! Our website has its own scale and more than 11,000 stations worldwide to provide you with the air quality of your city and answer the question of whether it is good to ventilate. Our scale consists of 10, 8 or 6 Points to make it easy for you to use it.

# Our Goal
The goal of this project was to visualize the air quality in a room and to find the right time of day when it is low. We built an interface that shows the current air quality to give you the optimal time for lüften.

# Our Technology
wann-soll-ich-lüften.de is an open source program which helps you with your search for the perfect time open your windows and to get fresh air again. Our program has been written in HTML, JavaScript, Python and Bootstrap and connects with our server which only uses the data we need.
