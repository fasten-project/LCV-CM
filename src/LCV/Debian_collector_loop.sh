
hs=`hostname`

for i in {0..10}
do
  python3 Debian_license_collector.py > logs_debian/$hs/"$(date +"%Y_%m_%d_%I_%M").log"
  echo "Running $i cycle"
  sleep 100
done
