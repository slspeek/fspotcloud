VERSION=$(sed -ne '2p' app.yaml |cut -d: -f2)
NEXTVERSION=$(($VERSION + 1))
sed -i -e "/version:/ s/$VERSION/ $NEXTVERSION/" app.yaml

