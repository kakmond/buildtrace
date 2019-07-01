# buildtrace

## Debian iso download URL  
https://cdimage.debian.org/debian-cd/current-live/ i386 or amd86 /iso-hybrid/  
吉上使用iso：debian-live-9.6.0-XXXX-xfce.iso  

## 大まかな流れ  
ソースパッケージを保管するためのtempディレクトリを　mkdir temp で作成
sourceList.txtとsource_download.pyを同じ階層に置き，source_download.pyを実行する（tempディレクトリの一つ上の階層）
お好みでsource_build_one.pyかsource_build.pyを実行する

## 各ファイルの説明

### sourceList.txt

	各行にソースパッケージのパッケージ名が記述されたテキストファイル  
  
### source_download.py  
	sourceList.txtに基づいて./tempディレクトリ内にソースパッケージをダウンロードする  
	1．ソースパッケージのダウンロードと2．ビルドに必要なソフトウェアのインストールを行なっている  
		1．sudo apt-get source パッケージ名  
		2．sudo apt-get build-dep -y パッケージ名  
	前提条件  
		1．./tempディレクトリが存在している  
		2．同階層にsourceList.txtファイルが存在している  
  
### source_build_one.py  
	提案手法をひとつのパッケージに適用させるときに使うファイル  
	キーボード入力でパッケージ名を受け取り./tempディレクトリ内を検索し，ビルドを実行する  
		dpkg-buildpackage -us -uc -b  
	strace.pyと同階層に存在している必要がある  
  
### source_build.py  
	提案手法をsourceList.txtに記述されている複数のパッケージに適用するときに使うファイル  
	strace.pyと同階層に存在している必要がある  
	  
### strace.py  
	提案手法を実装しているファイル  
	メイン関数はビルドコマンドとパッケージ名をstringで受け取る  
	結果のログの出力先は/buildTrace/パッケージ名ディレクトリ内  
	ディレクトリ構成は以下のとおり  

```
/  
└ buildTrace  
　 └ パッケージ名  
　 　 　 ├ backup  
　 　 　 │ ├ input  
　 　 　 │ │ └ ...many backup files...  
　 　 　 │ ├ output  
　 　 　 │ │ └ ...many backup files...  
　 　 　 │ ├ command  
　 　 　 │ │ └ buildCommand.txt  
　 　 　 │ └ hash  
　 　 　 │   ├ hash_all.txt  
　 　 　 │   ├ input_hash_list.txt  
　 　 　 │   ├ input_hash_only.txt  
　 　 　 │   ├ output_hash_list.txt  
　 　 　 │   └ output_hash.only.txt  
　 　 　 └ logs  
　 　 　 　 ├ input_all.txt  
　 　 　 　 ├ input_file_exist.txt  
　 　 　 　 ├ output_all.txt  
　 　 　 　 ├ output_file_exist.txt  
　 　 　 　 ├ ...many strace logs...  
　 　 　 　 └ times  
　 　 　 　 　 └ exeTimes.txt  
```

## 各ディレクトリ，ファイルの説明

	backup:記録者が保管しておくべき情報が入っているディレクトリ  
		input:入力ファイルのバックアップディレクトリ  
		output:出力ファイルのバックアップディレクトリ  
		command:ビルドに用いたコマンドのバックアップディレクトリ  
			buildCommand.txt:ビルドに用いたコマンドを記述したファイル  
		hash:計算したハッシュ値と関連情報を保存しているディレクトリ  
			hash_all.txt:ブロックチェーン上に記録する3つの代表ハッシュ値を記述したファイル  
			input_hash_list.txt:入力ファイルと計算したハッシュ値の関連を記述したファイル  
			input_hash_only.txt:input_hash_list.txtのハッシュ値のみを抽出し，ソートした結果を記述したファイル  
			output_hash_list.txt:出力ファイルと計算したハッシュ値の関連を記述したファイル  
			output_hash_only.txt:output_hash_list.txtのハッシュ値のみを抽出し，ソートした結果を記述したファイル  
	logs:straceのログや実行時間など検証に必要なものが入っているディレクトリ  
		input_all.txt:全てのstraceのログファイルから入力に関するファイルだけを抽出し，記述したファイル  
		input_file_exist.txt:input_all.txtの内，ビルド後に存在したファイルのみを記述したファイル  
		output_all.txt:全てのstraceのログファイルから出力に関するファイルだけを抽出し，記述したファイル  
		output_file_exist.txt:output_all.txtの内，ビルド後に存在したファイルのみを記述したファイル  
		times:実行時間のログ格納用ディレクトリ（ディレクトリにしなくてもよかったかも？）  
			exeTimes.txt:実行時間を記述したファイル  
		  
