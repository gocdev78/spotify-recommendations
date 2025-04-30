while [ "$status" != "STARTUP_FINISHED" ]
do
  sleep 10;
  echo "Checking if file /tmp/STARTUP_FINISHED exists...";
  status=$(gcloud compute ssh --zone europe-central2-a spotify-vm -- 'ls /tmp | grep STARTUP_FINISHED');
done

echo "File found, startup finished!";