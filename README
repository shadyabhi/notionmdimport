# NotionMDImport

## Intro

I created this simple script to import my local filesystem based markdown files to Notion.
I used directories to categorize my markdown files and there is no tool as of the day of writing to import multiple directories containing markdown files to Notion.

Two libraries that I would like to thank that made this job super easy:- 

* notion-py
* md2notion

## Usage

```
$ notionmdimport --basepage https://www.notion.so/newwiki-8b19791c9b974224a46e036d939da259 \
    --localwiki tests/testdata/wiki \ 
	--token_v2 token_super_secret
```

* `basepage`: Base page should already exist. It's the root of all wiki documents
* `localwiki`: Local path on the filesystem that contains the markdown files in various directories
* `token_v2`: The `token_v2` cookie for notion.so website
