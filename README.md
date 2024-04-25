# SETUP

```
docker build -t mydb .
```

```
docker run -it -p 5432:5432 mydb
```

Password: docker
```
psql -h localhost -p 5432 -U docker -d docker
```

```
\\i init.sql
```

```
exit
```

```
pip install -r requirements.txt
```

```
python3 load.py
```
