###
Every time someone tweets, log it to the console.

More at https://hub.storyscript.io/service/twitter
###


twitter stream as t
    when t tweet as tweet
        log info msg:tweet
