#!/bin/bash

# NOTE: NOT a good idea to run this script with all URLs, you WILL get your IP blocked by azlyrics
urls=("/lyrics/drake/thrillisgone.html"
"/lyrics/drake/tothefloor.html"
"/lyrics/drake/toomuch.html"
"/lyrics/drake/trophies.html"
"/lyrics/drake/trustissues.html"
"/lyrics/drake/tryharder.html"
"/lyrics/drake/tuscanleather.html"
"/lyrics/drake/undergroundkings.html"
"/lyrics/drake/underdog.html"
"/lyrics/drake/unforgettable.html"
"/lyrics/drake/unstoppable.html"
"/lyrics/drake/upallnight.html"
"/lyrics/drake/uptown.html"
"/lyrics/drake/usedto.html"
"/lyrics/drake/videogirl.html"
"/lyrics/drake/wemadeitfreestyle.html"
"/lyrics/drake/wellbefine.html"
"/lyrics/drake/wednesdaynightinterlude.html"
"/lyrics/drake/whatifikissedyou.html"
"/lyrics/drake/whatyouneed.html"
"/lyrics/drake/wheretonow.html"
"/lyrics/drake/wherewereyou.html"
"/lyrics/drake/worstbehavior.html"
"/lyrics/drake/wutangforever.html"
"/lyrics/drake/yamahamama.html"
"/lyrics/drake/youthe6.html"
"/lyrics/drake/youknowyouknow.html"
"/lyrics/drake/zone.html")

for url in ${urls[@]}; do
    curl -H "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2593.0 Safari/537.36" http://www.azlyrics.com/$url >> out
done
