#!/usr/bin/env python

# Import our facebook python SDK
import facebook
import json # Grab our JSON lib too
import os
import random
from time import sleep

# Define our Facebook Access Token
access_token = os.getenv('FB_ACCESS_TOKEN')

if not access_token:
    exit("""ERROR!: You must set an access token.
        Try setting the FB_ACCESS_TOKEN environment variable""")

# Define our "thank you" message
thankyou_messages = [
    'Thank you!! :D',
    'Thanks so much!',
    'Thanks!',
    'Thank you! I appreciate it!'
]

# Define our ridiculous "birthday" query
birthday_fql = ("SELECT post_id, actor_id, target_id, created_time, message, comments "
                "FROM stream "
                "WHERE source_id = me() "
                    "AND filter_key = 'others' "
                    "AND created_time > 1391346000 "
                    "AND actor_id != me() "
                    "AND comments.count = 0 "
                    "AND comments.can_post = 1 "
                    "AND (strpos(message, 'birthday') >= 0 "
                        "OR strpos(message, 'Birthday') >= 0 "
                        "OR strpos(message, 'happy') >= 0 "
                        "OR strpos(message, 'Happy') >= 0) "
                "LIMIT 500")

# Create a new GraphAPI instance with our access token
graph = facebook.GraphAPI(access_token)

# Grab our birthday posts using our FQL query
query_result = graph.get_object('fql', q=birthday_fql)

# Grab the data from the response
birthday_posts = query_result['data']

# Report how many posts we found...
print 'Query returned', len(birthday_posts), 'results'
print

# Create a counter, because why not?
posts_responded_to = 0;

# Let's loop through all of our returned posts
for post in birthday_posts:
    # Grab the post's ID
    post_id = post['post_id']

    # "Like" the post
    graph.put_object(post_id, 'likes')

    # Get a random message from the list
    rand_message = random.choice(thankyou_messages)

    # Post the comment on the post
    graph.put_object(post_id, 'comments', message=rand_message)

    # Increment our counter..
    posts_responded_to += 1

    # Print to keep track
    print 'The like/comment should have posted for post', post_id

    # Sleep for a bit to try and keep from getting rate limited
    sleep(0.1) # Sleep for a tenth of a second

# Let's get this "likes" steez going

# Report how many we've operated on..
print
print 'Responded to', posts_responded_to, 'posts'

# Fin
print 'Done.'
