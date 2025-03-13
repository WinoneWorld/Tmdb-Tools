# Tmdb-Tools

通过Tmdb API功能实现Tmdb个人列表数据导出CSV！目前已支持Trakt，Letterboxd......

Use the Tmdb API function to export Tmdb personal list data to CSV! Trakt, Letterboxd......


Tmdb API获取方式请自行谷歌！列表ID为列表网址后数字，例如https://www.themoviedb.org/list/123456-XXXXX，列表ID为123456

How to get the Tmdb API, please google it yourself! The list ID is the number after the list URL, for example, https://www.themoviedb.org/list/123456-XXXXX, the list ID is 123456


如果您想将您的Tmdb数据转移至Trakt，但是不知道如何操作，请仔细阅读以下步骤：

由于Tarkt平台限制，csv导入方式并不方便，我们更推荐您使用Letterboxd作为中间媒介！
首先：注册您的TmdbApi，将您需要转换的个人列表设置为公开可见状态！
使用Letterboxd_Export工具，它将引导您导出csv文件！
注册Letterboxd账号，创建个人列表，在创建时选择导入csv文件！
目前根据测试，电影可以使用导出的csv文件直接导入，电视剧可能需要您将csv文件中tmdb_id一列删除以更好匹配
但是由于Letterboxd收录原因，部分电视剧还是无法获取到，您可以选择截图记录好，后续手动录入！

感谢您的使用！
