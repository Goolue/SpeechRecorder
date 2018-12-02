cd /home/pi/programming/SpeechRecorder
echo "present working dir is:"
pwd | cat
echo ""

echo "pulling git"
git pull
echo ""

echo "git status is:"
git status | cat
echo ""

echo "running the script now!"
python -m listener.listener