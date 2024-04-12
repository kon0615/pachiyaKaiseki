保存先のテーブルのクエリ



CREATE TABLE [dbo].[アナスロ元データ](
	[年月日] [nvarchar](20) NULL,
	[店舗名] [nvarchar](50) NULL,
	[地域名] [nvarchar](50) NULL,
	[台番号] [int] NULL,
	[機種名] [nvarchar](50) NULL,
	[G数] [int] NULL,
	[差枚] [int] NULL,
	[BB] [int] NULL,
	[RB] [int] NULL,
	[合成確率] [nvarchar](50) NULL,
	[BB確率] [nvarchar](50) NULL,
	[RB確率] [nvarchar](50) NULL,
	[データ作成年月日] [nvarchar](20) NULL,
	[ART] [int] NULL,
	[ART確率] [nvarchar](50) NULL
) ON [PRIMARY]



長時間実行しているとプロセスがたまりPCがクラッシュします。
