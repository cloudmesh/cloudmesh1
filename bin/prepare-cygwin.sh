echo "# #####################################################################"
echo "# preparing cygwin for cloudmesh" 
echo "# #####################################################################"
echo "WARNING: not yet tested"

pip install python-ldap \
   --global-option=build_ext \
   --global-option="-I$(xcrun --show-sdk-path)/usr/include/sasl"

