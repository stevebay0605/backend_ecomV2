# 📸 Configuration ImgBB (Alternative à Cloudinary)

ImgBB est une alternative **GRATUITE et SIMPLE** à Cloudinary pour héberger les images.

## ✅ Avantages
- 🆓 **Gratuit** (uploads illimités)
- 🚀 **Aucune configuration** complexe
- 🔗 **URLs permanentes**
- ⚡ **Très simple** à mettre en place

## 📋 Étapes de configuration

### 1. Obtenir une clé API ImgBB (1 minute)

1. Va sur **https://api.imgbb.com/**
2. Clique sur **"Get API Key"**
3. Connecte-toi ou crée un compte (gratuit)
4. Copie ta clé API (format: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

### 2. Ajouter la clé sur Render

1. Va sur **Render Dashboard** → Ton service backend
2. **Environment** → **Add Environment Variable**
3. Ajoute :
   ```
   Key: IMGBB_API_KEY
   Value: ta-cle-api-imgbb
   ```
4. **Save Changes**

Render va redéployer automatiquement (2-3 minutes).

### 3. Vérifier dans les logs

Après redéploiement, les logs doivent afficher :
```
✅ ImgBB actif
```

### 4. Tester

1. Va sur `https://steveapi.onrender.com/admin/products/product/`
2. Édite un produit
3. Upload une image
4. Sauvegarde
5. L'image sera uploadée sur ImgBB et l'URL sera automatiquement enregistrée

## 🔄 Migrer depuis Cloudinary

Si tu as déjà des images sur Cloudinary, réupload-les simplement via l'admin Django.
Les nouvelles images iront automatiquement sur ImgBB.

## ⚙️ Comparaison

| Caractéristique | ImgBB | Cloudinary |
|----------------|-------|------------|
| Prix gratuit | ✅ Illimité | ⚠️ Limité |
| Configuration | ✅ 1 variable | ⚠️ 3 variables |
| Complexité | ✅ Très simple | ⚠️ Moyenne |
| Transformation images | ❌ Non | ✅ Oui |
| CDN | ✅ Oui | ✅ Oui |

## 🆘 Support

Si ImgBB ne marche pas, tu peux toujours utiliser Cloudinary en configurant les 3 variables :
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`

Le système détecte automatiquement lequel utiliser.
