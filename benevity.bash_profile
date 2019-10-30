
# The next line updates PATH for the Google Cloud SDK.
source '/Users/dwalters/google-cloud-sdk/path.bash.inc'

# The next line enables shell command completion for gcloud.
source '/Users/dwalters/google-cloud-sdk/completion.bash.inc'

# Setting PATH for Python 3.4
# The orginal version is saved in .bash_profile.pysave
#PATH="/Library/Frameworks/Python.framework/Versions/3.4/bin:${PATH}"
#export PATH

# Setting PATH for Python 3.7
#PATH=""

if [ -f /Users/dwalters/Source/git/contrib/completion/git-prompt.sh ]; then
. /Users/dwalters/Source/git/contrib/completion/git-prompt.sh
fi

#  Customize BASH PS1 prompt to show current GIT repository and branch.
#  by Mike Stewart - http://MediaDoneRight.com

#  SETUP CONSTANTS
#  Bunch-o-predefined colors.  Makes reading code easier than escape sequences.
#  I don't remember where I found this.

# Reset
Color_Off="\[\033[0m\]"       # Text Reset

# Regular Colors
Black="\[\033[0;30m\]"        # Black
Red="\[\033[0;31m\]"          # Red
Green="\[\033[0;32m\]"        # Green
Yellow="\[\033[0;33m\]"       # Yellow
Blue="\[\033[0;34m\]"         # Blue
Purple="\[\033[0;35m\]"       # Purple
Cyan="\[\033[0;36m\]"         # Cyan
White="\[\033[0;37m\]"        # White

# Bold
BBlack="\[\033[1;30m\]"       # Black
BRed="\[\033[1;31m\]"         # Red
BGreen="\[\033[1;32m\]"       # Green
BYellow="\[\033[1;33m\]"      # Yellow
BBlue="\[\033[1;34m\]"        # Blue
BPurple="\[\033[1;35m\]"      # Purple
BCyan="\[\033[1;36m\]"        # Cyan
BWhite="\[\033[1;37m\]"       # White

# Underline
UBlack="\[\033[4;30m\]"       # Black
URed="\[\033[4;31m\]"         # Red
UGreen="\[\033[4;32m\]"       # Green
UYellow="\[\033[4;33m\]"      # Yellow
UBlue="\[\033[4;34m\]"        # Blue
UPurple="\[\033[4;35m\]"      # Purple
UCyan="\[\033[4;36m\]"        # Cyan
UWhite="\[\033[4;37m\]"       # White

# Background
On_Black="\[\033[40m\]"       # Black
On_Red="\[\033[41m\]"         # Red
On_Green="\[\033[42m\]"       # Green
On_Yellow="\[\033[43m\]"      # Yellow
On_Blue="\[\033[44m\]"        # Blue
On_Purple="\[\033[45m\]"      # Purple
On_Cyan="\[\033[46m\]"        # Cyan
On_White="\[\033[47m\]"       # White

# High Intensty
IBlack="\[\033[0;90m\]"       # Black
IRed="\[\033[0;91m\]"         # Red
IGreen="\[\033[0;92m\]"       # Green
IYellow="\[\033[0;93m\]"      # Yellow
IBlue="\[\033[0;94m\]"        # Blue
IPurple="\[\033[0;95m\]"      # Purple
ICyan="\[\033[0;96m\]"        # Cyan
IWhite="\[\033[0;97m\]"       # White

# Bold High Intensty
BIBlack="\[\033[1;90m\]"      # Black
BIRed="\[\033[1;91m\]"        # Red
BIGreen="\[\033[1;92m\]"      # Green
BIYellow="\[\033[1;93m\]"     # Yellow
BIBlue="\[\033[1;94m\]"       # Blue
BIPurple="\[\033[1;95m\]"     # Purple
BICyan="\[\033[1;96m\]"       # Cyan
BIWhite="\[\033[1;97m\]"      # White

# High Intensty backgrounds
On_IBlack="\[\033[0;100m\]"   # Black
On_IRed="\[\033[0;101m\]"     # Red
On_IGreen="\[\033[0;102m\]"   # Green
On_IYellow="\[\033[0;103m\]"  # Yellow
On_IBlue="\[\033[0;104m\]"    # Blue
On_IPurple="\[\033[10;95m\]"  # Purple
On_ICyan="\[\033[0;106m\]"    # Cyan
On_IWhite="\[\033[0;107m\]"   # White

# Various variables you might want for your PS1 prompt instead
Time12h="\T"
Time12a="\@"
PathShort="\w"
PathFull="\W"
NewLine="\n"
Jobs="\j"


# PS1 snippet adopted from code for MAC/BSD : http://allancraig.net/index.php?option=com_content&view=article&id=108:ps1-export-command-for-git&catid=45:general&Itemid=96

export PS1=$IBlack$Time12h$Color_Off'$(git branch &>/dev/null;\
if [ $? -eq 0 ]; then \
  echo "$(echo `git status` | grep "nothing to commit" > /dev/null 2>&1; \
  if [ "$?" -eq "0" ]; then \
    # @4 - Clean repository - nothing to commit
    echo "'$Green'"$(__git_ps1 " (%s)"); \
  else \
    # @5 - Changes to working tree
    echo "'$IRed'"$(__git_ps1 " {%s}"); \
  fi) '$BYellow$PathShort$Color_Off'\$ "; \
else \
  # @2 - Prompt when not in GIT repo
  echo " '$Yellow$PathShort$Color_Off'\$ "; \
fi)'

alias iso_date="date '+%Y-%m-%dT%H:%M:%S'"
alias re_tag="ctags -e -R ."
alias sauce_tunnel="/Users/dwalters/bin/sc-4.5.4-osx/bin/sc -u benevity-webdev -k fc8441f9-581a-4060-a196-33f3c3ddcb8a -i deifante-tunnel --dns=127.0.0.1"
alias my_jenkins="java -Djavax.net.ssl.trustStore=/Users/dwalters/.jenkins/.keystore/cacerts -Djavax.net.ssl.trustStorePassword=changeit -jar /usr/local/Cellar/jenkins/2.105/libexec/jenkins.war --httpPort=8095"
alias sudo_emacs="sudo /Applications/Emacs.app/Contents/MacOS/Emacs"

export NVM_DIR="/Users/dwalters/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm
# NVM
if [ -s ~/.nvm/nvm.sh ]; then
	NVM_DIR=~/.nvm
	source ~/.nvm/nvm.sh
fi

JENKINS_HOME=/Users/dwalters/.jenkins
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_74.jdk/Contents/Home
export PATH="/usr/local/opt/node@10/bin:$PATH"
export PATH="/usr/local/opt/icu4c/bin:$PATH"
export PATH="/usr/local/opt/icu4c/sbin:$PATH"
export PATH="/Users/dwalters/.ebcli-virtual-env/executables:$PATH"
export PATH="/Users/dwalters/Library/Python/3.7/bin:$PATH"
export PATH="/Users/dwalters/Projects/py_scripts:$PATH"
export PATH="/Users/dwalters/Projects/shell_scripts:$PATH"
export PATH="/Users/dwalters/bin:$PATH"


# Initializes your local Terraform cache; clones external modules and providers
alias tfinit="terraform init"
 
# Create a Terraform plan file, and displays the pending changes. Creating plan files allows you to keep a record of your plans.
alias tfplan="terraform plan -out ~/ops/tfplans/\$(basename \$(pwd))_\$(date +%F_%H_%M_%S).tfplan"
 
# Apply the most recent Terraform plan file, and create resources
alias tfapply="terraform apply ~/ops/tfplans/\$(ls -w1t ~/ops/tfplans | head -1)"
 
 
#################################################################################
# <Benevity AWS General>
 
# export credentials to your terminal environment, allowing helper tools to connect
function aws-get-profile-parameter() {
    profile="${1?Please provide an AWS profile to configure.}"
    param="${2?Please provide a parameter to fetch.}"
    if ! aws configure --profile "$profile" get "$param" 2>/dev/null
    then
        >&2 echo "ERROR: Failed to retrieve [$param] for profile [$profile]."
    fi
}
 
# create new credentials (if needed) with the help of Okta
function aws-auth() {
    v="${AWS_PROFILE?Please define an AWS_PROFILE variable to continue.}"
    rm -f ~/.okta/.current-session && touch ~/.okta/$profile
    ln -s ~/.okta/$AWS_PROFILE ~/.okta/.current-session
    echo "Authenticating as "$OKTA_AWS_ROLE_TO_ASSUME
 
    env OKTA_PROFILE=$AWS_PROFILE java \
        -Djava.util.logging.config.file=~/.okta/logging.properties \
        -classpath ~/.okta/okta-aws-cli.jar \
        com.okta.tools.WithOkta echo -n ""
 
    export AWS_ACCESS_KEY_ID=$(aws-get-profile-parameter "$profile" "aws_access_key_id") &&
    export AWS_SECRET_ACCESS_KEY=$(aws-get-profile-parameter "$profile" "aws_secret_access_key") &&
    export AWS_SESSION_TOKEN=$(aws-get-profile-parameter "$profile" "aws_session_token") &&
    export AWS_SECURITY_TOKEN=$AWS_SESSION_TOKEN;
}
 
# check my identity
function aws-whoami() {
    aws sts get-caller-identity
}
 
# things are weird, refresh my current session
function aws-refresh() {
    v="${AWS_PROFILE?Please define an AWS_PROFILE variable to continue.}"
    rm -f ~/.okta/$AWS_PROFILE
    aws-auth
    aws-whoami
}
 
# things are broken, destroy and recreate my session
function aws-reset() {
    v="${AWS_PROFILE?Please define an AWS_PROFILE variable to continue.}"
    rm -f ~/.okta/.current-session ~/.okta/cookies.properties ~/.okta/profiles ~/.okta/$AWS_PROFILE
    aws-auth
    aws-whoami
}
 
# get a list of running instances ("aws-list" or filter with "aws-list platform")
function aws-list() {
    if [[ -n $1 ]]; then
        filter="--filters \"Name=instance-state-name,Values=running\" \"Name=tag:Name,Values=*$1*\""
    else
        filter="--filters \"Name=instance-state-name,Values=running\""
    fi
    eval "aws ec2 describe-instances ${filter} --query \"Reservations[].Instances[].{Ip:PrivateIpAddress,State:State.Name,Name:Tags[?Key=='Name'].Value|[0],Id:InstanceId}|sort_by(@,&Name)[]\" --output table"
}
 
# start a ssm session ("ash i-0a503e0c181c888f0")
function ash() {
    aws ssm start-session --target $1
}
 
 
##############################################################################
# <AWS Environments>
 
 
function aws-product-poc() {
    export AWS_ACCOUNT_ID="983430949435"
    export AWS_DEFAULT_REGION="us-east-1"
    export AWS_PROFILE="benevity_product_poc"
    export OKTA_AWS_ROLE_TO_ASSUME="arn:aws:iam::"$AWS_ACCOUNT_ID":role/ProductPocAdminIdp"
 
    aws-auth
    aws-whoami
}
 
 
function aws-sre-qa() {
    export AWS_ACCOUNT_ID="933128491709"
    export AWS_DEFAULT_REGION="us-east-1"
    export AWS_PROFILE="benevity_sre_qa"
    export OKTA_AWS_ROLE_TO_ASSUME="arn:aws:iam::"$AWS_ACCOUNT_ID":role/SreQaAdminIdp"
 
    aws-auth
    aws-whoami
}
 
 
# </AWS Environments>
##############################################################################
