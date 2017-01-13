.DEFAULT_GOAL = all

.PHONY :  all install make_dir run

all : | install make_dir run

install: 
	pip install -r requirements.txt

make_dir:
	sudo mkdir /ramdisk -p
	sudo mount -t tmpfs -o size=512m tmpfs /ramdisk;

run:
	scrapy crawl jd -o db.csv -t csv
