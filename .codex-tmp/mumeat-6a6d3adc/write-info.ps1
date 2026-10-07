$body = @'
大家好,我是一个在北美写代码的程序员👨‍💻

过去几个月,我下班后一直在做一个给孕期和坐月子妈妈用的食谱工具,叫 MumEat(妈妈吃)。今天第一次拿出来讲。

起因很简单:我发现怀孕的朋友每天最头疼的不是产检,是「今天吃什么」——

😵 国内的孕期食谱,食材在美国超市买不到
😵 网上的营养建议东一条西一条,还互相打架
😵 家里做饭的人不知道孕妇能吃啥,天天瞎猜

作为程序员,我的本能是:这不就是个能用程序解决的问题吗?于是有了 MumEat:

✅ 输入孕周 / 产后周,自动排一周 21 餐(图 2)
✅ 每道菜标清关键营养素:铁、钙、DHA、叶酸(图 3)
✅ 自动生成购物清单,Costco / 大华一趟买齐
✅ 全是中式家常菜,做法写得连我都会

⚠️ 说句实话:它还很早期,肯定有不完善的地方。所以我特别想找一批**正在孕期或坐月子的妈妈**,帮我一起把它打磨好——你用得顺不顺、卡在哪、想要什么功能,都直接告诉我,我一条条改。

🎁 内测的妈妈我会一对一陪着用,后面也会有些小福利感谢你们。

想参与的,评论区扣「内测」或者私信我都可以😊 也欢迎先随手关注,看着它一点点变好~
'@
$links = @(
'https://sns-img-bd.xhscdn.com/spectrum/1040g34o323abhqq274005p9hv62amv3scmhrrc0?imageView2/format/jpg',
'https://sns-img-bd.xhscdn.com/spectrum/1040g34o323abhqq2740g5p9hv62amv3s3g542so?imageView2/format/jpg',
'https://sns-img-bd.xhscdn.com/spectrum/1040g34o323abhqq274105p9hv62amv3sdqa7c3g?imageView2/format/jpg'
)
function E([string]$s) { [System.Net.WebUtility]::HtmlEncode($s) }
$bodyXml = (E $body.Trim()).Replace("`r`n",'<br/>').Replace("`n",'<br/>')
$url = 'https://www.xiaohongshu.com/explore/6a6d3adc0000000005021240?xsec_token=AB0kinWMJ-ShxUbUsP4c9Qrmr3rCLyO3JFY1LYhfdRRvw=&xsec_source=pc_search'
$info = '<title>笔记信息</title><h1>笔记信息</h1><ul>'
$info += '<li><b>笔记ID：</b>6a6d3adc0000000005021240</li>'
$info += '<li><b>笔记链接：</b><a href="'+(E $url)+'">打开原笔记</a></li>'
$info += '<li><b>笔记类型：</b>图文</li>'
$info += '<li><b>笔记标题：</b>我做了个孕妈食谱工具,想找准妈妈提提建议</li>'
$info += '<li><b>笔记正文：</b>'+$bodyXml+'</li>'
$info += '<li><b>Hashtag：</b>#北美妈妈 #孕期食谱 #月子餐 #海外孕妈 #孕期营养 #独立开发者 #程序员做产品</li>'
$info += '<li><b>博主ID：</b>6531f984000000002a037c7c</li>'
$info += '<li><b>博主昵称：</b>MumEat</li>'
$info += '<li><b>点赞量：</b>54</li><li><b>收藏量：</b>48</li><li><b>评论量：</b>75</li><li><b>分享量：</b>41</li>'
$info += '<li><b>发布时间：</b>2026-08-01 08:16</li><li><b>更新时间：</b>2026-09-27 07:14</li>'
$info += '<li><b>图片数量：</b>3</li><li><b>采集时间：</b>2026-10-02</li>'
$info += '<li><b>笔记封面链接：</b><a href="'+(E $links[0])+'">打开原图</a></li>'
$info += '<li><b>笔记图片文档：</b><a href="https://my.feishu.cn/wiki/C5LGwawFji5WIqkL6ZRcbzpNnph">笔记图片文档</a></li></ul>'
$info += '<h2>笔记图片链接</h2><ul>'
for($i=0;$i -lt $links.Count;$i++){ $n=$i+1; $info += '<li><a href="'+(E $links[$i])+'">第'+$n+'张原图</a></li>' }
$info += '</ul>'
Set-Content -LiteralPath '.codex-tmp/mumeat-6a6d3adc/info.xml' -Value $info -Encoding utf8 -NoNewline
