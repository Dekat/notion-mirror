# Notion Mirror

This app is a mirror of Notion website, giving the user a better accessibility.

Currently, we can only read pages and not edit them.

## Install and launch

### Prerequisite

Copy the file `.env.tpl` to `.env` and replace needed values in there.

Your personal token can be found by seeing cookies sent when crawling Notion website.
The cookie looks like it :
```
token_v2: d8b00087ba0af014dc44b7361b9065ac9255b625edea3d4fdd77ca22d7681b03072a692eacff0ab606d5f81c4897ccf6906847ce25fdd37f313e4e52501f2151c297910b0b9d717fe0b3a55a6d15
```

Space ID can be found by reading parameters sent to Notion API when getting a "block"
and logged in. In the JSON data sent, you can find this entry :
```
{
  spaceId: “4489c211-09d6-4069-ae3b-1665e25d6c03”,
}
```

### Via Docker

- Just launch with this command : `make run`

### Native

- Install `pipenv` : `pip install pipenv`
- Install dependencies : `pipenv install --deploy --dev`
- Launch it : `pipenv run python manage.py run`

## Usage

Open your web browser and build the URL of the page you want to see :

`http://<your_local_app_ip>:<your_local_app_port>/page/<page_id>`

`page_id` is an hexadecimal number of 32 characters 
(ie: `298da9ef60b04dfc83535dace8a58dbf`) always findable at any Notion page URL.

## Next development steps

- [ ] Add a cache, which updates pages only if an update is detected
- [ ] Handle arrays (exported as CSV file)
- [ ] Add a front client, enabling async requests to API
- [ ] Add the same sidebar as the one of Notion
- [ ] Add other useful infos on page
- [ ] Enable possibility to write data
