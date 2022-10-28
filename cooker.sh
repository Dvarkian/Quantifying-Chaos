
#Clear the previous data
rm -r "cooked_data"
mkdir "cooked_data"

mkdir "cooked_data/angles"
mkdir "cooked_data/angles_polar"
for file in raw_data/angles/*.csv
do
    python3 cooking/cooker.py $file  cooked_data/angles/ cooked_data/angles_polar/
done

mkdir "cooked_data/propogation"
mkdir "cooked_data/propogation_polar"
for file in raw_data/propogation/*.csv
do
    python3 cooking/cooker.py $file  cooked_data/propogation/ cooked_data/propogation_polar/
done

mkdir "cooked_data/weights"
mkdir "cooked_data/weights_polar"
for file in raw_data/weights/*.csv
do
    python3 cooking/cooker.py $file  cooked_data/weights/ cooked_data/weights_polar/
done