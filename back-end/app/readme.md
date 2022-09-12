## 后端代码说明

### 目录结构

- crud：操作数据库代码。

- models：*orm*相关代码。

  - 可以使用`sqlacodegen`生成，如:

    ```shell
    sqlacodegen "mysql://root:123456@localhost:3306/threat_intelligence" --tables ip_alarm_event --outfile ".\back-end\app\models\ip.py"
    ```

    注：若表中含有多个外键，定义`relationship`时需要显式定义参数`foreign_keys`。

- schemas：传输结构体定义代码，即`Pydantic`对象。

- api：接口代码。

  - 推荐使用`APIRouter`，将各实体api分类。

- dependencies.py：依赖注入相关代码。

- database.py：数据库相关