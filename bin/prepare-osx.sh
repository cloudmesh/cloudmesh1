echo "# #####################################################################"
echo "# preparing OSX for cloudmesh" 
echo "# #####################################################################"
echo "WARNING: not yet tested"

echo "# ----------------------------------------------------------------------"
echo "# set the ARCHFLAG to ignore non existing flags"
echo "# ----------------------------------------------------------------------"

export ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future 

echo "# ----------------------------------------------------------------------"
echo "# install brew"
echo "# ----------------------------------------------------------------------"
ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

echo "# ----------------------------------------------------------------------"
echo "# install freetype"
echo "# ----------------------------------------------------------------------"
brew install freetype
ln -s /usr/local/opt/freetype/include/freetype2 /usr/local/include/freetype
