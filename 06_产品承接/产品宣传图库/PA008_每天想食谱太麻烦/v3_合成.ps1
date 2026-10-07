Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $MyInvocation.MyCommand.Path
function Rounded([float]$x,[float]$y,[float]$w,[float]$h,[float]$r) {
$p=[System.Drawing.Drawing2D.GraphicsPath]::new()
$p.AddArc($x,$y,$r*2,$r*2,180,90); $p.AddArc($x+$w-$r*2,$y,$r*2,$r*2,270,90)
$p.AddArc($x+$w-$r*2,$y+$h-$r*2,$r*2,$r*2,0,90); $p.AddArc($x,$y+$h-$r*2,$r*2,$r*2,90,90)
$p.CloseFigure(); return $p
}
$canvas=[System.Drawing.Bitmap]::new((Join-Path $root 'v3_背景文字层.png'))
$source=[System.Drawing.Bitmap]::new((Join-Path $root '用户提供_横版原图.png'))
$g=[System.Drawing.Graphics]::FromImage($canvas)
$g.SmoothingMode=[System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.TextRenderingHint=[System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
# Composite original device pixels without regenerating screen content.
for($i=20;$i -ge 1;$i--){
$p=Rounded (86-$i/2) (655-$i/3) (913+$i) (1200+$i) 77
$b=[System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(2,40,22,55))
$g.FillPath($b,$p);$b.Dispose();$p.Dispose()
}
$clip=Rounded 86 650 913 1200 76
$g.SetClip($clip)
$g.DrawImage($source,[System.Drawing.Rectangle]::new(86,650,913,971),[System.Drawing.Rectangle]::new(810,58,830,883),[System.Drawing.GraphicsUnit]::Pixel)
$g.ResetClip();$clip.Dispose()
# Floating promotional share button, independent of preserved app UI.
$state=$g.Save()
$g.TranslateTransform(794,1128);$g.RotateTransform(-6)
for($i=18;$i -ge 1;$i--){
$p=Rounded (-225-$i/2) (-74+$i/2) (450+$i) (148+$i) 30
$b=[System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(3,52,25,72))
$g.FillPath($b,$p);$b.Dispose();$p.Dispose()
}
$p=Rounded -225 -80 450 148 28
$g.FillPath([System.Drawing.Brushes]::White,$p);$p.Dispose()
$p=Rounded -205 -60 410 108 20
$b=[System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#8351B9'))
$g.FillPath($b,$p);$p.Dispose();$b.Dispose()
$pen=[System.Drawing.Pen]::new([System.Drawing.Color]::White,5)
$pen.StartCap=[System.Drawing.Drawing2D.LineCap]::Round
$pen.EndCap=[System.Drawing.Drawing2D.LineCap]::Round
$g.DrawLine($pen,-164,9,-164,-14);$g.DrawLine($pen,-164,9,-121,9);$g.DrawLine($pen,-121,9,-121,-8)
$g.DrawLine($pen,-148,-8,-126,-29);$g.DrawLine($pen,-126,-29,-145,-29);$g.DrawLine($pen,-126,-29,-126,-10)
$font=[System.Drawing.Font]::new('Microsoft YaHei',44,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
$fmt=[System.Drawing.StringFormat]::new()
$fmt.Alignment=[System.Drawing.StringAlignment]::Center
$fmt.LineAlignment=[System.Drawing.StringAlignment]::Center
$g.DrawString('分享给家人',$font,[System.Drawing.Brushes]::White,[System.Drawing.RectangleF]::new(-107,-60,290,108),$fmt)
$font.Dispose();$fmt.Dispose();$pen.Dispose()
$g.Restore($state);$g.Dispose()
$canvas.Save((Join-Path $root 'PA008_每天想食谱太麻烦_v3.png'),[System.Drawing.Imaging.ImageFormat]::Png)
$small=[System.Drawing.Bitmap]::new(390,520)
$sg=[System.Drawing.Graphics]::FromImage($small);$sg.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$sg.DrawImage($canvas,0,0,390,520);$sg.Dispose()
$small.Save((Join-Path $root 'v3_手机尺寸检查.png'),[System.Drawing.Imaging.ImageFormat]::Png)
$small.Dispose();$canvas.Dispose();$source.Dispose()

