#! /bin/sh 

# config git 

git config --global user.name "argo-mm-generator"
git config --global user.email "argo-mm-generator@stackmeister.com"

echo "Clone argocd repo" 

git clone https://$USERNAME:$PASSWORD@$ARGOCD_REPO_URL /app/tmp/argocd 

echo "Clone wiki repo" 

git clone https://$USERNAME:$PASSWORD@$WIKI_REPO_URL /app/tmp/wiki

echo "" > /app/tmp/wiki/$WIKI_PATH/argoCD.md

echo -e "# Do not edit this File! This file is auto-generated by the ArgoCD preSync Hook\n" >> /app/tmp/wiki/$WIKI_PATH/argoCD.md
echo -e "The argocd apps will be installed in following order with sync-waves:\n" >> /app/tmp/wiki/$WIKI_PATH/argoCD.md
echo -e ":::mermaid\n" >> /app/tmp/wiki/$WIKI_PATH/argoCD.md

python3 /app/argo-mm-generator.py >> /app/tmp/wiki/$WIKI_PATH/argoCD.md 

echo ":::" >> /app/tmp/wiki/$WIKI_PATH/argoCD.md

cd /app/tmp/wiki

git add . 
git commit -m "Update argoCD.md"
git push
