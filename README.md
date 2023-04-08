# vk_content_poster
The service for auto posting messages with attachments in a vk group

# Instructions

## Getting VK API token

https://dvmn.org/encyclopedia/qna/63/kak-poluchit-token-polzovatelja-dlja-vkontakte/

## run

Run run.bat to post all images from memes/ . They will be posted and moved to posted/ .

Run install_vk.bat to install vk python module

## settings

create file settings json with content like:

    {
        "ACCESS_TOKEN": "YOUR_VK_API_ACCESS_TOKEN",
        "POSTING_TIME_LIST": "13:00,18:00",
        "RANDOM_POSTING": true,
        "SKIP_DAYS": "5,6",
        "GROUP_ID":  "YOUR_VK_GROUP_ID",
        "API_VERSION": "5.131"
    }
POSTING_TIME_LIST - daily posting time list, must contain 1 or more values

RANDOM_POSTING - randomly shuffle files before posting

SKIP_DAYS - days of week to skip posting (from MONDAY = 0 to SUNDAY = 6)

API_VERSION - vk api version
