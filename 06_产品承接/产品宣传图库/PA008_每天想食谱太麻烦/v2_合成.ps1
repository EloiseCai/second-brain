Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $MyInvocation.MyCommand.Path
$source=[System.Drawing.Bitmap]::new((Join-Path $root '用户提供_横版原图.png'))
$layer=[System.Drawing.Bitmap]::new((Join-Path $root 'v2_文字底图.png'))
$canvas=[System.Drawing.Bitmap]::new(1086,1448)
$g=[System.Drawing.Graphics]::FromImage($canvas)
$g.Clear([System.Drawing.Color]::FromArgb(250,248,252))
$g.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.DrawImage($layer,[System.Drawing.Rectangle]::new(0,120,500,1197),[System.Drawing.Rectangle]::new(0,0,605,1448),[System.Drawing.GraphicsUnit]::Pixel)
# Preserve the entire original tablet region, including all UI text and numbers.
$g.DrawImage($source,[System.Drawing.Rectangle]::new(512,430,574,591),[System.Drawing.Rectangle]::new(806,50,866,891),[System.Drawing.GraphicsUnit]::Pixel)
$g.Dispose()
$canvas.Save((Join-Path $root 'PA008_每天想食谱太麻烦_v2.png'),[System.Drawing.Imaging.ImageFormat]::Png)
$preview=[System.Drawing.Bitmap]::new(390,520)
$pg=[System.Drawing.Graphics]::FromImage($preview)
$pg.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$pg.DrawImage($canvas,0,0,390,520)
$pg.Dispose()
$preview.Save((Join-Path $root 'v2_手机尺寸检查.png'),[System.Drawing.Imaging.ImageFormat]::Png)
$preview.Dispose()
$canvas.Dispose()
$layer.Dispose()
$source.Dispose()

