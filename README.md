Fork of TorrentBOX to add Docker support and additional functionality.

# TorrentBOX
Multi-user based torrent download and sharing application written in Django  

## Screenshot
![Demo](https://cloud.githubusercontent.com/assets/8179234/17862249/670f204e-68cf-11e6-81e8-feb0214786dc.png)

## Quick Start
* On first run:

```bash
docker-compose up -d
docker-compose exec web makemigrations
docker-compose exec torrentbox makemigrations
docker-compose exec web migrate
docker-compose exec torrentbox migrate
docker-compose exec web createsuperuser
```

Afterwards, you can simply run with:

```bash
docker-compose up
```

**NOTE:** This is only for test. If you want to deploy it, use Django with other web servers like [Apache](http://www.apache.org/) or [Nginx](http://nginx.org/).

## License
[MIT](LICENSE.md)
