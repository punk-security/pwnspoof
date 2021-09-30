from datetime import timedelta, datetime
from models import Session
import random
from string import ascii_lowercase


default_user_agents = [
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/91.0.4472.124+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/746",
    "Mozilla/4.0+(compatible;+MSIE+6.0)",
    "Mozilla/5.0+(Windows+NT+6.1;+WOW64)+AppleWebKit/537.1+(KHTML,+like+Gecko)+Chrome/21.0",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/74.0.3729.169+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+WOW64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/72.0.3626.121+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/74.0.3729.157+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/60.0.3112.113+Safari/537.36",
    "Mozilla/5.0+(X11;+Linux+x86_64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/44.0.2403.157+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+6.1;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/60.0.3112.90+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/72.0.3626.121+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+6.1;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/74.0.3729.169+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+5.1)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/46.0.2490.71+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+6.1;+WOW64)+AppleWebKit/537.1+(KHTML,+like+Gecko)+Chrome/21.0.1180.83+Safari/537.1",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/69.0.3497.100+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/63.0.3239.132+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/80.0.3987.149+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/79.0.3945.88+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/78.0.3904.108+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/90.0.4430.212+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+5.1;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/60.0.3112.90+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+6.2;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/60.0.3112.90+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/79.0.3945.130+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/85.0.4183.121+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/84.0.4147.105+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/90.0.4430.93+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+6.3;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/60.0.3112.113+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/87.0.4280.88+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/67.0.3396.99+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/83.0.4103.116+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/88.0.4324.104+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/81.0.4044.138+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/91.0.4472.124+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/80.0.3987.132+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/87.0.4280.141+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/74.0.3729.131+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/68.0.3440.106+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/72.0.3626.121+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/85.0.4183.102+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/86.0.4240.198+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+6.1;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/79.0.3945.88+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/84.0.4147.135+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/65.0.3325.181+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/80.0.3987.163+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/91.0.4472.77+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/88.0.4324.190+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+6.1;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/69.0.3497.100+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+6.1)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/56.0.2924.76+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/64.0.3282.186+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+6.1;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/63.0.3239.132+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/70.0.3538.102+Safari/537.36",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/57.0.2987",
    "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/61.0.3163",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_2+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Mobile/15E148Webkit+based+browser",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_2+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/12.1+Mobile/15E148+Safari/604.1+Safari+12.1",
    "Outlook-iOS/709.2226530.prod.iphone+(3.24.1)+Outlook",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_1_4+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Mobile/16D57Webkit+based+browser",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+13_3_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/13.0.5+Mobile/15E148+Safari/604.1+Safari+13",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+13_3+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/13.0.4+Mobile/15E148+Safari/604.1+Safari+13",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_3+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Mobile/15E148Webkit+based+browser",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+13_5_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/13.1.1+Mobile/15E148+Safari/604.1+Safari+13.1",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_2+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Webkit+based+browser",
    "Outlook-iOS/709.2189947.prod.iphone+(3.24.0)+Outlook",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+14_4+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/14.0.3+Mobile/15E148+Safari/604.1+Safari+14",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+14_4_2+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/14.0.3+Mobile/15E148+Safari/604.1+Safari+14",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+13_1_3+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/13.0.1+Mobile/15E148+Safari/604.1+Safari+13",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+14_2+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/14.0.1+Mobile/15E148+Safari/604.1+Safari+14",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+10_0+like+Mac+OS+X)+AppleWebKit/602.4.6+(KHTML,+like+Gecko)+Version/10.0+Mobile/14A346+Safari/E7FBAF+Safari+10",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+14_3+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/14.0.2+Mobile/15E148+Safari/604.1+Safari+14",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+13_4_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/13.1+Mobile/15E148+Safari/604.1+Safari+13.1",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_4_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/12.1.2+Mobile/15E148+Safari/604.1+Safari+12.1",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_3_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/12.1.1+Mobile/15E148+Safari/604.1+Safari+12.1",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+14_6+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/14.1.1+Mobile/15E148+Safari/604.1+Safari+14.1",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+11_4_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/11.0+Mobile/15E148+Safari/604+1+Safari+11",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+14_4+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Mobile/15E148+Webkit+based+browser",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+13_6_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/13.1.2+Mobile/15E148+Safari/604.1+Safari+13.1",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+13_7+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/13.1.2+Mobile/15E148+Safari/604.1+Safari+13.1",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+13_6+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/13.1.2+Mobile/15E148+Safari/604.1+Safari+13.1",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/12.0+Mobile/15E148+Safari/604+Safari+12",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_4+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/12.1.2+Mobile/15E148+Safari/604.1+Safari+12.1",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+11_4_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Mobile/15G77+Webkit+based+browser",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+14_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/14.0+Mobile/15E148+Safari/604+1+Safari+14",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+14_0_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/14.0+Mobile/15E148+Safari/604+1+Safari+14",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+11_3+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/11.0+Mobile/15E148+Safari/604+1+Safari+11",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+10_3_3+like+Mac+OS+X)+AppleWebKit/603.3.8+(KHTML,+like+Gecko)+Version/10.0+Mobile/14G60+Safari/602+1+Safari+10",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_0_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/12.0+Mobile/15E148+Safari/604+1+Safari+12",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+13_1_2+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/13.0.1+Mobile/15E148+Safari/604+1+Safari+13",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+11_4+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/11.0+Mobile/15E148+Safari/604+1+Safari+11",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_1_2+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Mobile/16C101+Webkit+based+browser",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+11_2_6+like+Mac+OS+X)+AppleWebKit/604.5.6+(KHTML,+like+Gecko)+Version/11.0+Mobile/15D100+Safari/604+1+Safari+11",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+13_2_3+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/13.0.3+Mobile/15E148+Safari/604+1+Safari+13",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+10_2_1+like+Mac+OS+X)+AppleWebKit/602.4.6+(KHTML,+like+Gecko)+Version/10.0+Mobile/14D27+Safari/602+1+Safari+10",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_3_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Mobile/15E148+Webkit+based+browser",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+14_4_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/14.0.3+Mobile/15E148+Safari/604+1+Safari+14",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+9_0+like+Mac+OS+X)+AppleWebKit/601.1.46+(KHTML,+like+Gecko)+Version/9.0+Mobile/13A344+Safari+E7FBAFSafari+9",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+14_0+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/14.0+Mobile/15E148+Safari/604+1+Safari+14",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_0+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/12.0+Mobile/15E148+Safari/604+1+Safari+12",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+10_0+like+Mac+OS+X)+AppleWebKit/602.1.50+(KHTML,+like+Gecko)+Version/10.0+YaBrowser/17.4.3.195.10+Mobile/14A346+Safari/E7FBAF+Yandex+Browser+17.4",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_1_4+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Version/12.0+Mobile/15E148+Safari/604+1+Safari+12",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+12_0_1+like+Mac+OS+X)+AppleWebKit/605.1.15+(KHTML,+like+Gecko)+Mobile/16A404+Webkit+based+browser",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+10_3_2+like+Mac+OS+X)+AppleWebKit/603.2.4+(KHTML,+like+Gecko)+Version/10.0+Mobile/14F89+Safari/602+1+Safari+10",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+9_1+like+Mac+OS+X)+AppleWebKit/601.1.46+(KHTML,+like+Gecko)+Version/9.0+Mobile/13B143+Safari/601+1+Safari+9",
    "Mozilla/5.0+(iPhone;+CPU+iPhone+OS+11_0+like+Mac+OS+X)+AppleWebKit/604.1.38+(KHTML,+like+Gecko)+Version/11.0",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.1.4322)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1)",
    "Mozilla/5.0+(Windows+NT+6.1;+WOW64;+Trident/7.0;+rv:11.0)+like+Gecko",
    "Mozilla/5.0+(compatible;+MSIE+9.0;+Windows+NT+6.1;+WOW64;+Trident/5.0;+KTXN)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1)",
    "Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+6.0)",
    "Mozilla/5.0+(Windows+NT+10.0;+WOW64;+Trident/7.0;+rv:11.0)+like+Gecko",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.1.4322;+.NET+CLR+2.0.50727)",
    "Mozilla/4.0+(compatible;+MSIE+9.0;+Windows+NT+6.1;+125LA;+.NET+CLR+2.0.50727;+.NET+CLR+3.0.04506.648;+.NET+CLR+3.5.21022)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+.NET+CLR+1.1.4322)",
    "Mozilla/5.0+(Windows+NT+6.1;+Trident/7.0;+rv:11.0)+like+Gecko",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.0)",
    "Mozilla/4.0+(compatible;+MSIE+9.0;+Windows+NT+6.1)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+98)",
    "Mozilla/5.0+(Windows+NT+6.3;+WOW64;+Trident/7.0;+rv:11.0)+like+Gecko",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.0;+.NET+CLR+1.1.4322)",
    "Mozilla/5.0+(compatible;+MSIE+9.0;+Windows+NT+6.1;+WOW64;+Trident/5.0)",
    "Mozilla/5.0+(compatible;+MSIE+9.0;+Windows+NT+6.1;+Win64;+x64;+Trident/5.0)",
    "Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+5.1;+.NET+CLR+1.1.4322)",
    "Mozilla/5.0+(compatible;+MSIE+10.0;+Windows+NT+6.2)",
    "Mozilla/5.0+(compatible;+MSIE+9.0;+Windows+NT+6.1;+Trident/5.0)",
    "Mozilla/5.0+(compatible;+MSIE+10.0;+Windows+NT+6.1;+WOW64;+Trident/6.0)",
    "Mozilla/5.0+(compatible;+MSIE+10.0;+Windows+NT+6.1;+Trident/6.0)",
    "Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+6.0;+SLCC1;+.NET+CLR+2.0.50727;+Media+Center+PC+5.0;+.NET+CLR+3.0.04506)",
    "Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+5.1)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+.NET+CLR+1.0.3705)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.1.4322;+InfoPath.1)",
    "Mozilla/4.0+(compatible;+MSIE+5.01;+Windows+NT+5.0)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.0.3705)",
    "Mozilla/5.0+(Windows+NT+10.0;+WOW64;+Trident/7.0;+Touch;+rv:11.0)+like+Gecko",
    "Mozilla/5.0+(Windows+NT+10.0;+WOW64;+Trident/7.0;+.NET4.0C;+.NET4.0E;+.NET+CLR+2.0.50727;+.NET+CLR+3.0.30729;+.NET+CLR+3.5.30729;+rv:11.0)+like+Gecko",
    "Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+6.0;+WOW64;+Trident/4.0;+SLCC1;+.NET+CLR+2.0.50727;+.NET+CLR+3.5.30729;+.NET+CLR+3.0.30729;+.NET4.0C;+.NET4.0E)",
    "Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+5.1;+.NET+CLR+1.1.4322;+.NET+CLR+2.0.50727)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.0.3705;+.NET+CLR+1.1.4322)",
    "Mozilla/5.0+(compatible,+MSIE+11,+Windows+NT+6.3;+Trident/7.0;+rv:11.0)+like+Gecko",
    "Mozilla/5.0+(compatible;+MSIE+10.0;+Windows+NT+6.2;+WOW64;+Trident/6.0)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+2.0.50727)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+InfoPath.1)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.1.4322;+.NET+CLR+2.0.50727;+InfoPath.1)",
    "Mozilla/5.0+(Windows+NT+6.1;+Win64;+x64;+Trident/7.0;+rv:11.0)+like+Gecko",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+FunWebProducts;+.NET+CLR+1.1.4322)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.0.3705;+.NET+CLR+1.1.4322;+Media+Center+PC+4.0)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+98;+Win+9x+4.90)",
    "Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+5.1;+.NET+CLR+2.0.50727;+.NET+CLR+1.1.4322)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.1.4322;+InfoPath.1;+.NET+CLR+2.0.50727)",
    "Mozilla/5.0+(compatible;+MSIE+9.0;+Windows+NT+6.0;+Trident/5.0)",
    "Mozilla/4.0+(compatible;+MSIE+5.0;+Windows+98;+DigExt)",
    "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+FunWebProducts)",
    "Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0)",
    "Mozilla/4.0+(compatible;+MSIE+7.0;+Windows+NT+6.1;+WOW64;+Trident/7.0;+SLCC2;+.NET+CLR+2.0.50727;+.NET+CLR+3.5.30729;+.NET+CLR+3.0.30729;+Media+Center+PC+6.0;+.NET4.0C;+.NET4.0E)",
]

default_geos = {
    "GB": 200,
    "DE": 1,
    "FR": 1,
    "IT": 1,
    "NL": 1,
}

hour_profile = {
    0: 1,
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 2,
    6: 5,
    7: 10,
    8: 15,
    9: 15,
    10: 10,
    11: 10,
    12: 15,
    13: 15,
    14: 10,
    15: 10,
    16: 5,
    17: 5,
    18: 15,
    19: 20,
    20: 15,
    21: 10,
    22: 5,
    23: 2,
}


def ExpandWeightDictToList(d):
    if type(d) != dict:
        raise ValueError("should be a dictionary of values and weight")
    l = []
    for k in d.keys():
        l += [k] * d[k]
    return l


def SessionGenerator(
    num_sessions,
    app,
    start_date,
    end_date,
    average_duration_mins=30,
    duration_deviation_mins=5,
    user_agents=default_user_agents,
    geos=default_geos,
    hour_profile=hour_profile,
    max_sessions_per_user=5,
):
    geos = ExpandWeightDictToList(geos)
    hours = ExpandWeightDictToList(hour_profile)
    end_date = end_date - timedelta(
        minutes=average_duration_mins + duration_deviation_mins
    )
    i = 0
    for x1 in range(num_sessions):
        i += 1
        activity_patterns = list(app.activity_patterns())
        duration = random.randint(
            average_duration_mins - duration_deviation_mins,
            average_duration_mins + duration_deviation_mins,
        )
        sd = RandomDatetime(start_date, end_date, hours)
        username = "".join(random.choice(ascii_lowercase) for i in range(2)) + str(
            random.randint(100000, 999999)
        )
        s1 = Session(
            start_datetime=sd,
            geo=random.choice(geos),
            duration_mins=duration,
            activity_patterns=activity_patterns,
            user_agent=random.choice(user_agents),
            username=username,
            noise_interactions=app.noise_interactions,
        )
        yield s1
        # Add additional user sessions
        remaining_potential_user_sessions = max_sessions_per_user - 1
        if remaining_potential_user_sessions:
            remaining_user_sessions = random.randint(
                0, remaining_potential_user_sessions
            )
        else:
            remaining_user_sessions = 0
        if remaining_user_sessions:
            for x2 in range(remaining_user_sessions):
                activity_patterns = list(app.activity_patterns())
                duration = random.randint(
                    average_duration_mins - duration_deviation_mins,
                    average_duration_mins + duration_deviation_mins,
                )
                sd = RandomDatetime(start_date, end_date, hours)
                yield Session(
                    start_datetime=sd,
                    source_ip=s1.source_ip,
                    duration_mins=duration,
                    activity_patterns=activity_patterns,
                    user_agent=s1.user_agent,
                    username=username,
                    noise_interactions=app.noise_interactions,
                )
                i += 1
        if i > num_sessions:
            return


def RandomDatetime(start, end, hours_list):
    max_delta = end - start
    days_delta = timedelta(days=random.randint(0, max_delta.days))
    hours_delta = timedelta(hours=random.choice(hours_list))
    minutes_delta = timedelta(minutes=random.randint(0, 59))
    delta = days_delta + hours_delta + minutes_delta
    return start + delta
