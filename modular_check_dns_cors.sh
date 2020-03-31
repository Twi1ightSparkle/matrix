#!/bin/zsh

# Exit if not all required arguments are passed
if [ -z "$1" ] || [ -z "$2" ]; then
      echo "    Two arguments is required: hostname domain. The third is optional: riotSubDomain"
      echo "    Example: ./modular_check_dns_cors.sh twily01-staging twily.me riot"
      echo "    (In Mongo, the hostname here is saved under serverConfig.host)/n"
      exit 1
fi


# Define vars
print_https="no"
print_dig="no"
print_client="no"
print_server="no"
client_missing="no"
server_missing="no"
host=$1
domain=$2
if [ ! -z $3 ]; then
    riot=$3
fi
riot_url="${riot}.${domain}"
client_url="https://$domain/.well-known/matrix/client"
server_url="https://$domain/.well-known/matrix/server"
client_should_contain="{\"m.homeserver\":{\"base_url\":\"https://$host.modular.im\"},\"m.identity_server\":{\"base_url\":\"https://vector.im\"}}"
server_should_contain="{\"m.server\":\"$host.modular.im:443\"}"


# Test CNAME corrct
if [ ! -z $3 ]; then
    dig_command="dig +short $riot_url CNAME"
    dig_result=$(eval $dig_command)
    cname_should_be="$host.riot.im."

    if [ $dig_result = $cname_should_be ]; then
        echo -e "\e[32mCNAME is correctly configured.\e[0m"
    else
        echo -e "\e[31mProblem: CNAME for $riot_url is not correctly configured.\e[0m"
        print_dig="yes"
    fi
fi


# Test if HTTPS
if wget --spider $client_url 2>/dev/null; then
    echo -e "\e[32m$domain has HTTPS enabled.\e[0m"
else
    echo -e "\e[31mProblem: HTTPS must be enabled for $domain\e[0m"
    print_https="yes"
fi


# Make sure client exist
if [ "$(curl --silent --location $client_url)" ]; then
    # Make sure client har correct content
    if [ "$(curl --silent --location $client_url | tr -d '[:space:]')" = $client_should_contain ]; then
        echo -e "\e[32m$client_url is accessible and contain the correct data.\e[0m"
    else
        echo -e "\e[31mProblem: $client_url does not contain the correct data.\n\t(this might also mean it's not accessible, but the server is serving some error page)\e[0m"
        print_client="yes"
    fi
else
    echo -e "\e[31mProblem: $client_url is not accessible.\e[0m"
fi


# Make sure server exist
if [ "$(curl --silent --location $server_url)" ]; then
    # Make sure server har correct content
    if [ "$(curl --silent --location $server_url | tr -d '[:space:]')" = $server_should_contain ]; then
        echo -e "\e[32m$server_url is accessible and contain the correct data.\e[0m"
    else
        echo -e "\e[31mProblem: $server_url does not contain the correct data\n\t(this might also mean it's not accessible, but the server is serving some error page).\e[0m"
        print_server="yes"
    fi
else
    echo -e "\e[31mProblem: $server_url is not accessible.\e[0m"
fi


# Test CORS headers for client
if [ "$(curl --include --silent --location --header 'Origin: curl-test.twily.me' $client_url | awk '{print tolower($0)}' | grep 'access-control-allow-origin: *')" ]; then
    echo -e "\e[32mCORS is enabled for $client_url.\e[0m"
else
    echo -e "\e[31mProblem: CORS must be enabled for $client_url.\e[0m"
fi


# Print full dig result if not pass for troubleshooting
if [ ! -z $3 ]; then
    if [ $print_dig = "yes" ]; then
        echo "\n\nDig reults for $domain:"
        dig_command="dig $riot_url CNAME"
        dig_result=$(eval $dig_command)
        echo $dig_result
    fi
fi


# Print HTTPS if not pass
if [ $print_https = "yes" ]; then
    echo "\n\nOutput of https spider:"
    echo $(wget --spider $client_url)
fi


# Print client if not pass
if [ $print_client = "yes" ]; then
    echo "\n\n$client_url should contain:\nBut it does contain:"
    echo $(echo $client_should_contain)
    echo $(curl --silent --location $client_url | tr -d '[:space:]')
fi


# Print server if not pass
if [ $print_server = "yes" ]; then
    echo "\n\n$server_url should contain:\nBut it does contain:"
    echo $(echo $server_should_contain)
    echo $(curl --silent --location $server_url | tr -d '[:space:]')
fi