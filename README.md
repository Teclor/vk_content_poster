# vk_content_poster
The service for auto posting messages with attachments in a vk group

# Instructions

## run

Run run.bat to post all images from memes/ . They will be posted and moved to posted/ .

Run install_vk.bat to install vk python module

## settings

create file settings json with content like:

    {
        "ACCESS_TOKEN": "YOUR_VK_API_ACCESS_TOKEN",
        "POSTING_TIME": "17:00",
        "GROUP_ID":  "YOUR_VK_GROUP_ID",
        "API_VERSION": "5.131"
    }
POSTING_TIME - daily posting time

API_VERSION - vk api version
