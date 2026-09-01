# External Skills

## guizang-social-card-skill

- Repository: https://github.com/op7418/guizang-social-card-skill
- Purpose: generate Xiaohongshu/Rednote social-card sets and WeChat 21:9 + 1:1 cover pairs.
- Integration point: `skills/social-cover-generator/SKILL.md`
- Project adapter: `prompts/social-cover-generator.md` and `workflows/social-cover-generation-flow.md`
- Rendering model: HTML/CSS seed templates rendered through a browser screenshot workflow; the upstream skill does not lock a specific image-generation model.

Install or update outside this repository with:

```bash
npx skills add https://github.com/op7418/guizang-social-card-skill --skill guizang-social-card-skill
```

The upstream skill must remain separate from this repository's adapter. Do not copy generated task folders into the upstream skill root.
