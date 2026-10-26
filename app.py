import streamlit as st
from gtts import gTTS
import os
import random
import time

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA Y ESTILOS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Nihongo Quiz", page_icon="🇯🇵", layout="centered")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 3em;
        font-size: 18px !important;
        border-radius: 10px;
    }
    .kanji-display {
        font-size: 54px;
        text-align: center;
        font-weight: bold;
        margin: 20px 0;
        color: #1E293B;
    }
    .hiragana-display {
        font-size: 36px;
        text-align: center;
        margin: 15px 0;
        color: #2563EB;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BASE DE DATOS DE VOCABULARIO POR CATEGORÍAS (ACTUALIZADA)
# -----------------------------------------------------------------------------
if "vocab_categories" not in st.session_state:
    st.session_state.vocab_categories = {
        "🌤️ Clima": [
            {"kanji": "地震", "reading": "じしん", "meaning": "terremoto"},
            {"kanji": "壊れる", "reading": "こわれる", "meaning": "romperse,averiarse,malograrse,destruirse,colapsar(se usa para equipos, muñecos, casas, es muy versatil)"},
            {"kanji": "状況", "reading": "じょうきょう", "meaning": "situación,circunstancias,estado o momento (de lo que pasa alrededor)"},
            {"kanji": "状態", "reading": "じょうたい", "meaning": "estado, condición (de algo o alguien)"},
            {"kanji": "起こる", "reading": "おこる", "meaning": "ocurrir"},
            {"kanji": "経つ", "reading": "たつ", "meaning": "tiempo transcurrido desde que ocurrió algo"},
            {"kanji": "降る", "reading": "ふる", "meaning": "caer(lluvia, nieve)"},
            {"kanji": "溢れる", "reading": "あふれる", "meaning": "desbordar,rebosar(rios,rostro que desborda alegria)"},
            {"kanji": "気象庁", "reading": "きしょうちょう", "meaning": "Agencia Meteorológica de Japón"},
            {"kanji": "非常に", "reading": "ひじょうに", "meaning": "extremadamente,muy (非常に強い台風, por ejemplo)"},
            {"kanji": "最大", "reading": "さいだい", "meaning": "máximo"},
            {"kanji": "風速", "reading": "ふうそく", "meaning": "velocidad del viento"},
            {"kanji": "最大風速", "reading": "さいだいふうそく", "meaning": "máxima velocidad del viento"},
            {"kanji": "次第に", "reading": "しだいに", "meaning": "gradualmente"},
            {"kanji": "離れる", "reading": "はなれる", "meaning": "alejarse"},
            {"kanji": "(に)注意する", "reading": "ちゅういする", "meaning": "tener cuidado, prestar atención"},
            {"kanji": "(に)警戒する", "reading": "けいかいする", "meaning": "estar alerta,mantenerse vigilante"},
            {"kanji": "勢力", "reading": "せいりょく", "meaning": "fuerza, potencia"},
            {"kanji": "空気", "reading": "くうき", "meaning": "aire"},
            {"kanji": "おそれ", "reading": "おそれ", "meaning": "riesgo"},
            {"kanji": "湿った空気", "reading": "しめったくうき", "meaning": "aire húmedo"},
            {"kanji": "不安定", "reading": "ふあんてい", "meaning": "inestable"},
            {"kanji": "大気", "reading": "たいき", "meaning": "atmósfera"},
            {"kanji": "激しい", "reading": "はげしい", "meaning": "intensa,fuerte,violento"},
            {"kanji": "範囲", "reading": "はんい", "meaning": "zona o área, rango, alcance"},
            {"kanji": "現地", "reading": "げんち", "meaning": "lugar donde ocurrió algo o un incidente"},
            {"kanji": "割れる", "reading": "われる", "meaning": "romperse,agrietada(ventanas,vidrios, ceramicas)"},
            {"kanji": "晴れる", "reading": "はれる", "meaning": "despejarse, estar soleado"},
            {"kanji": "備える", "reading": "そなえる", "meaning": "prepararse para un desastre,instalar muebles"},
            {"kanji": "近づく", "reading": "ちかづく", "meaning": "acercarse"},
            {"kanji": "感段差", "reading": "かんだんさ", "meaning": "cambio de temperatura"},
            {"kanji": "予報", "reading": "よほう", "meaning": "pronóstico"}
        ],
        "🍳 Cocina": [
            {"kanji": "弱火/中火/強火", "reading": "よわび/ちゅうび/きょうび", "meaning": "fuego lento, fuego medio, fuego fuerte"},
            {"kanji": "加熱する", "reading": "かねつする", "meaning": "calentar"},
            {"kanji": "消す", "reading": "けす", "meaning": "apagar (luces, fuego), borrar (texto, archivos), extinguir o neutralizar (llama, olor, dolor)"},
            {"kanji": "火をつけて", "reading": "ひをつけて", "meaning": "prender el fuego"},
            {"kanji": "用意します", "reading": "よういします", "meaning": "preparar (comida, el plato para servir)"},
            {"kanji": "炊く", "reading": "たく", "meaning": "cocinar, cocer arroz o granos con agua"},
            {"kanji": "焼く", "reading": "やく", "meaning": "cocinar en un sentido mas amplio(sarten, hornilla,etc.)"},
            {"kanji": "薄スライスする", "reading": "うすスライスする", "meaning": "cortar finamente en rebanadas"},
            {"kanji": "濃い", "reading": "こい", "meaning": "oscuro(color),intenso(味が濃い),espeso o denso(salsas,niebla,etc)"},
            {"kanji": "魚介", "reading": "ぎょかい", "meaning": "productos marinos"},
            {"kanji": "食器", "reading": "しょっき", "meaning": "vasillas, platos, utensilios"},
            {"kanji": "材料", "reading": "ざいりょう", "meaning": "materiales, ingredientes (mas general)"},
            {"kanji": "食材", "reading": "しょくざい", "meaning": "ingredientes"},
            {"kanji": "混ぜる", "reading": "まぜる", "meaning": "mezclar"},
            {"kanji": "切る", "reading": "きる", "meaning": "cortar"},
            {"kanji": "揚げる", "reading": "あげる", "meaning": "freir"},
            {"kanji": "炒める", "reading": "いためる", "meaning": "saltear, sofreir"},
            {"kanji": "加える", "reading": "くわえる", "meaning": "añadir (agregas algo a otra cosa, haciendo que forme parte de ella)"},
            {"kanji": "追加する", "reading": "ついかする", "meaning": "añadir(añadir algo más a lo que ya existe, ejemplo: añadir pedido, añadir otra funcionalidad,etc.)"},
            {"kanji": "調味料", "reading": "ちょうみりょう", "meaning": "condimento"},
            {"kanji": "胡椒", "reading": "こしょう", "meaning": "pimienta"},
            {"kanji": "にんにく", "reading": "にんにく", "meaning": "ajo"},
            {"kanji": "火を弱める/強める", "reading": "ひをよわめる/つよめる", "meaning": "bajar el fuego, subir el fuego"},
            {"kanji": "少々", "reading": "しょうしょう", "meaning": "un poco, una pizca"},
            {"kanji": "新鮮", "reading": "しんせん", "meaning": "fresco"},
            {"kanji": "冷やす", "reading": "ひやす", "meaning": "enfriar"},
            {"kanji": "上質", "reading": "じょうしつ", "meaning": "alta calidad, fino (productos, materiales o experiencias que tienen un estándar muy elevado)"},
            {"kanji": "蕩ける", "reading": "とろける", "meaning": "derretirse(dentro de la boca)"},
            {"kanji": "臭い", "reading": "くさい", "meaning": "mal oliente"},
            {"kanji": "搾る", "reading": "しぼる", "meaning": "exprimir"},
            {"kanji": "食感", "reading": "しょっかん", "meaning": "textura"},
            {"kanji": "もう何もつけずに、何もかけずに", "reading": "もうなにもつけずに、なにもかけずに", "meaning": "sin ponerle ni hecharle nada"},
            {"kanji": "つぶす", "reading": "つぶす", "meaning": "aplastar, machacar"},
            {"kanji": "蓋をする", "reading": "ふたをする", "meaning": "tapar (con una tapa)"},
            {"kanji": "蒸し焼きにする", "reading": "むしやきにする", "meaning": "cocinar al vapor"},
            {"kanji": "味付けする", "reading": "あじつけする", "meaning": "sazonar"}
        ],
        "⚡ Adverbios Especiales": [
            {"kanji": "一旦", "reading": "いったん", "meaning": "por ahora, por un momento, una vez que..."},
            {"kanji": "日常", "reading": "にちじょう", "meaning": "habitualmente, en el dia a dia"},
            {"kanji": "一斉に", "reading": "いっせいに", "meaning": "simultáneamente, todos a la vez"},
            {"kanji": "気軽に", "reading": "きがるに", "meaning": "libremente, sin dudar(invitar a alguien a hacer algo con confianza)"},
            {"kanji": "一瞬で", "reading": "いっしゅんで", "meaning": "en un instante, en un abrir y cerrar de ojos"},
            {"kanji": "偶然", "reading": "ぐうぜん", "meaning": "por casualidad, por azar"},
            {"kanji": "微妙", "reading": "びみょう", "meaning": "regular, mas o menos"},
            {"kanji": "たっぷり", "reading": "たっぷり", "meaning": "lleno de …"},
            {"kanji": "パッと", "reading": "ぱっと", "meaning": "\"de golpe\" (acciones que ocurren rapidamente), \"de la nada\""},
            {"kanji": "ぐっと", "reading": "ぐっと", "meaning": "de un tiron(una bebida),contener una emoción, aumento de nivel notablemente"},
            {"kanji": "一応", "reading": "いちおう", "meaning": "por si acaso, por el momento (con una idea de precaucion), al menos..."},
            {"kanji": "[espacio/lugar] + 一面", "reading": "いちめん", "meaning": "por todo ese espacio / toda la superficie de ese lugar"},
            {"kanji": "[persona]+の,は+[adjetivo]+一面", "reading": "いちめん", "meaning": "una faceta..., un aspecto"},
            {"kanji": "[objeto]の一面", "reading": "いちめん", "meaning": "una parte, una cara de ese objeto"},
            {"kanji": "numerador+cont. de tiempo+ぶりに", "reading": "ぶりに", "meaning": "por primera vez en..."},
            {"kanji": "きっと", "reading": "きっと", "meaning": "seguramente"},
            {"kanji": "十分", "reading": "じゅうぶん", "meaning": "suficiente (十分な + sustantivo,十分に suficientemente)"},
            {"kanji": "Cantidad + ずつ", "reading": "ずつ", "meaning": "\"cada\" (一人に二個ずつ配ります), \"uno por uno\"(一人ずつ入ってください)"},
            {"kanji": "少しずつ", "reading": "すこしずつ", "meaning": "poco a poco, gradualmente"},
            {"kanji": "勝手に", "reading": "かってに", "meaning": "Sin permiso,por cuenta propia,como le da la gana"},
            {"kanji": "それぞれ(の)A", "reading": "それぞれのえー", "meaning": "cada A"},
            {"kanji": "のんびり + verbo", "reading": "のんびり", "meaning": "hacer algo tranquilamente"},
            {"kanji": "のんびりした + sustantivo", "reading": "のんびりした", "meaning": "expresión な-adjetival que modifica un sustantivo"},
            {"kanji": "必ず", "reading": "かならず", "meaning": "sin falta, definitivamente"},
            {"kanji": "ぴったり", "reading": "ぴったり", "meaning": "exactamente,precisamente,justo (con la idea de encajar, coincidir(tiempo,lugar,cantidad) o ajustarse perfectamente)"},
            {"kanji": "互いに", "reading": "たがいに", "meaning": "mutuamente"},
            {"kanji": "当時", "reading": "とうじ", "meaning": "en ese momento,en aquellos dias, en aquellas epocas"},
            {"kanji": "先に", "reading": "さきに", "meaning": "primero, por adelantado, antes(comparación con otro evento de que ocurre primero)"},
            {"kanji": "事前に", "reading": "じぜんに", "meaning": "con anticipación / de antemano"},
            {"kanji": "きちんと", "reading": "きちんと", "meaning": "correctamente"},
            {"kanji": "はっきり", "reading": "はっきり", "meaning": "claramente,evidentemente"},
            {"kanji": "ほとんどのA", "reading": "ほとんどのえー", "meaning": "la mayoría de A"},
            {"kanji": "いくつか+SUST", "reading": "いくつか", "meaning": "ALGUNOS.."},
            {"kanji": "少ない+SUST", "reading": "すくない", "meaning": "POCOS..."}
        ],
        "🚨 Crimen": [
            {"kanji": "行為", "reading": "こうい", "meaning": "acto, conducta"},
            {"kanji": "責任", "reading": "せきにん", "meaning": "responsabilidad, deber"},
            {"kanji": "負う", "reading": "おう", "meaning": "asumir(resp.), cargar(peso), incurrir(deudas, no crimen)"},
            {"kanji": "襲います", "reading": "おそいます", "meaning": "atacar, asaltar, azotar"},
            {"kanji": "逮捕する", "reading": "たいほする", "meaning": "arrestar"},
            {"kanji": "懲役を言い渡されます", "reading": "ちょうえきをいいわたされます", "meaning": "ser sentenciado, condenado a trabajo forzado"},
            {"kanji": "疑い", "reading": "うたがい", "meaning": "sospecha, duda"},
            {"kanji": "容疑者", "reading": "ようぎしゃ", "meaning": "sospechoso"},
            {"kanji": "隠れる", "reading": "かくれる", "meaning": "esconderse en"},
            {"kanji": "証拠", "reading": "しょうこ", "meaning": "pruebas, evidencia"},
            {"kanji": "傷をつける", "reading": "きずをつける", "meaning": "inflinjir, causar daño, heridas, lesión, rasguño a personas o objetos"},
            {"kanji": "押し付ける", "reading": "おしつける", "meaning": "imponer, presionar (trabajos, ideas molestas, etc.)"},
            {"kanji": "犯罪", "reading": "はんざい", "meaning": "delito"},
            {"kanji": "追います", "reading": "おいます", "meaning": "perseguir(sueño, metas,a alguien)"},
            {"kanji": "追われる", "reading": "おわれる", "meaning": "ser presionado, agobiado(por tiempo, obligaciones)"},
            {"kanji": "罪悪感を感じる", "reading": "ざいあかんをかんじる", "meaning": "sentir culpa"},
            {"kanji": "逃げる", "reading": "にげる", "meaning": "huir"},
            {"kanji": "泥棒", "reading": "どろぼう", "meaning": "ladron"},
            {"kanji": "事件", "reading": "じけん", "meaning": "evento, suceso, asunto criminal, caso, incidente"},
            {"kanji": "被害者", "reading": "ひがいしゃ", "meaning": "victima"},
            {"kanji": "加害者", "reading": "かがいしゃ", "meaning": "agresor"},
            {"kanji": "本人確認", "reading": "ほんにんかくにん", "meaning": "verificación de identidad"},
            {"kanji": "詳しく", "reading": "くわしく", "meaning": "detalladamente"},
            {"kanji": "含まれる", "reading": "ふくまれる", "meaning": "estar incluido o contenido"},
            {"kanji": "悪用する", "reading": "あくようする", "meaning": "hacer un uso indebido / utilizar con fines maliciosos"},
            {"kanji": "なりすます", "reading": "なりすます", "meaning": "suplantar identidad"},
            {"kanji": "詐欺", "reading": "さぎ", "meaning": "estafa, fraude"},
            {"kanji": "報道させる", "reading": "ほうどうさせる", "meaning": "ser reportado o difundido en las noticias o medios de comunicacion"},
            {"kanji": "誘い", "reading": "さそい", "meaning": "invitación"},
            {"kanji": "押収された", "reading": "おうしゅうされた", "meaning": "ser incautado,confiscado o decomisado"},
            {"kanji": "盗む", "reading": "ぬすむ", "meaning": "robar"},
            {"kanji": "手口", "reading": "てぐち", "meaning": "modus operandi,tecnica criminal"}
        ],
        "📈 Economía": [
            {"kanji": "限定商品", "reading": "げんていしょうひん", "meaning": "producto limitado"},
            {"kanji": "期間限定", "reading": "きかんげんてい", "meaning": "producto limitado por periodo"},
            {"kanji": "地域限定", "reading": "ちいきげんてい", "meaning": "producto limitado por región"},
            {"kanji": "消費者", "reading": "しょうひしゃ", "meaning": "consumidor"},
            {"kanji": "企業", "reading": "きぎょう", "meaning": "empresa"},
            {"kanji": "人手不足", "reading": "ひとでぶそく", "meaning": "falta de mano de obra"},
            {"kanji": "購入", "reading": "こうにゅう", "meaning": "compra"},
            {"kanji": "価格", "reading": "かかく", "meaning": "precio, costo (mas formal que 値段)"},
            {"kanji": "購入する", "reading": "こうにゅうする", "meaning": "adquirir, comprar"},
            {"kanji": "留まる", "reading": "とどまる", "meaning": "no pasar de cierto limite, detenerse (0.5%に留まる）"},
            {"kanji": "計算する", "reading": "けいさんする", "meaning": "calcular"},
            {"kanji": "料金", "reading": "りょうきん", "meaning": "tarifa, precio"},
            {"kanji": "経済", "reading": "けいざい", "meaning": "economía"},
            {"kanji": "決める", "reading": "きめる", "meaning": "fijar o establecer reglas, precios,limites|decidir algo|marcar un gol o marcar un punto"},
            {"kanji": "大盛況", "reading": "だいせいきょう", "meaning": "gran éxito(refiriéndose a eventos, espectáculos,negocios)"},
            {"kanji": "乗客", "reading": "じょうきゃく", "meaning": "pasajero"},
            {"kanji": "観客", "reading": "かんきゃく", "meaning": "espectador, publico"},
            {"kanji": "来客", "reading": "らいきゃく", "meaning": "visita"},
            {"kanji": "費用", "reading": "ひよう", "meaning": "gasto total"},
            {"kanji": "食費", "reading": "しょくひ", "meaning": "gasto de comida"},
            {"kanji": "交通費", "reading": "こうつうひ", "meaning": "gasto de transporte"},
            {"kanji": "光熱費", "reading": "こうねつひ", "meaning": "gasto de servicios basicos"},
            {"kanji": "医療費", "reading": "いりょうひ", "meaning": "gasto medicos"},
            {"kanji": "手数料", "reading": "てすうりょう", "meaning": "comision"},
            {"kanji": "予算", "reading": "よさん", "meaning": "presupuesto"},
            {"kanji": "お金を下す", "reading": "おかねをおろす", "meaning": "sacar dinero de una cuenta bancaria"},
            {"kanji": "銀行口座", "reading": "ぎんこうこうざ", "meaning": "cuenta bancaria"},
            {"kanji": "電子マネー", "reading": "でんしまねー", "meaning": "dinero electronico"},
            {"kanji": "お釣り", "reading": "おつり", "meaning": "el vuelto, cambio"},
            {"kanji": "価格差", "reading": "かかくさ", "meaning": "diferencia de precio"},
            {"kanji": "営業する", "reading": "えいぎょうする", "meaning": "operar, abierto al publico"},
            {"kanji": "営業時間", "reading": "えいぎょうじかん", "meaning": "horario de atencion"},
            {"kanji": "営業中", "reading": "えいぎょうちゅう", "meaning": "abierto (para negocios, se usa como el abierto que aparecen en la puerta)"},
            {"kanji": "営業の仕事", "reading": "えいぎょうのしごと", "meaning": "trabajo de ventas"},
            {"kanji": "合計で", "reading": "ごうけいで", "meaning": "en total(mas formal)"},
            {"kanji": "全部で", "reading": "ぜんぶで", "meaning": "en total"},
            {"kanji": "家賃", "reading": "やちん", "meaning": "alquiler, renta"},
            {"kanji": "節約する", "reading": "せつやくする", "meaning": "ahorrar, recortar costos"},
            {"kanji": "平均", "reading": "へいきん", "meaning": "en promedio"},
            {"kanji": "貯金", "reading": "ちょきん", "meaning": "ahorros"},
            {"kanji": "発売されます", "reading": "はつばいされます", "meaning": "ser lanzado a la venta"},
            {"kanji": "価値", "reading": "かち", "meaning": "valor, merito"},
            {"kanji": "開発する", "reading": "かいはつする", "meaning": "desarrollar"},
            {"kanji": "登場する", "reading": "とうじょうする", "meaning": "introducir, entrada(al mercado,en el escenario, etc.)"},
            {"kanji": "観光客", "reading": "かんこうきゃく", "meaning": "turista"},
            {"kanji": "占めました", "reading": "しめました", "meaning": "representar (un porcentaje), ocupar, adueñarse"},
            {"kanji": "販売される", "reading": "はんばいされる", "meaning": "estando a la venta"},
            {"kanji": "生産する", "reading": "せいさんする", "meaning": "fabricar"},
            {"kanji": "罰金", "reading": "ばっきん", "meaning": "multa"},
            {"kanji": "科される", "reading": "かされる", "meaning": "imponer, asignar, infligir (multa, pena o impuesto)"},
            {"kanji": "調査", "reading": "ちょうさ", "meaning": "investigación、encuesta（averiguar información sobre una situación concreta、notan científico, académico)"},
            {"kanji": "税金", "reading": "ぜいきん", "meaning": "impuestos"},
            {"kanji": "公開される", "reading": "こうかいされる", "meaning": "ser abierto al publico"},
            {"kanji": "(を)超える", "reading": "こえる", "meaning": "superar"},
            {"kanji": "割合", "reading": "わりあい", "meaning": "porcentaje, tasa"},
            {"kanji": "民間会社", "reading": "みんかんがいしゃ", "meaning": "empresa privada"},
            {"kanji": "民間", "reading": "みんかん", "meaning": "sector privado"},
            {"kanji": "助成する", "reading": "じょせいする", "meaning": "subvencionar"},
            {"kanji": "投資", "reading": "とうし", "meaning": "inversion"},
            {"kanji": "法人", "reading": "ほうじん", "meaning": "corporación"},
            {"kanji": "借金", "reading": "しゃっきん", "meaning": "deuda"},
            {"kanji": "利子", "reading": "りし", "meaning": "interés"},
            {"kanji": "数量限定", "reading": "すうりょうげんてい", "meaning": "edición limitada"},
            {"kanji": "売り切れ", "reading": "うりきれ", "meaning": "agotado"},
            {"kanji": "グッズ", "reading": "グッズ", "meaning": "artículos, mercancías o productos"},
            {"kanji": "輸入する", "reading": "ゆにゅうする", "meaning": "importar"},
            {"kanji": "産業", "reading": "さんぎょう", "meaning": "industria"},
            {"kanji": "市場", "reading": "しじょう", "meaning": "mercado"}
        ],
        "⚖️ Legal": [
            {"kanji": "対策", "reading": "たいさく", "meaning": "medida(安全対策を強化する,intensificar medidas de seguridad)"},
            {"kanji": "苦情", "reading": "くじょう", "meaning": "queja, reclamo formal"},
            {"kanji": "制度", "reading": "せいど", "meaning": "sistema, conj de leyes, normas (支援制度 sist de ayuda, 教育制度 sist educativo, 年金制度 sist de pensiones)"},
            {"kanji": "導入する", "reading": "どうにゅうする", "meaning": "implementar un sist o tecnologia"},
            {"kanji": "実施する", "reading": "じっしする", "meaning": "Llevar a cabo, ejecutar, poner en práctica o aplicar (plan, un examen, una ley, una encuesta, un experimento o un evento)"},
            {"kanji": "保険", "reading": "ほけん", "meaning": "seguro (健康保険 seguro medico, 任意保険 seguro de auto, 火災/地震保険 seguro contra incendio o terremotos, 生命保険 seguro de vida)"},
            {"kanji": "強制する", "reading": "きょうせいする", "meaning": "forzar, obligar o imponer ideas, es de carácter autoritario"},
            {"kanji": "資格", "reading": "しかく", "meaning": "título oficial, certificado o aptitud legal para hacer algo"},
            {"kanji": "妥協する", "reading": "だきょうする", "meaning": "Aceptar condiciones inferiores a las deseadas para llegar a un acuerdo (お互いに妥協する, 妥協点を見つける)"},
            {"kanji": "譲る", "reading": "ゆずる", "meaning": "ceder el paso o el asiento(道、席)、transferir una posesión, ceder en una discusión"},
            {"kanji": "財産", "reading": "ざいさん", "meaning": "bienes"},
            {"kanji": "不公平", "reading": "ふこうへい", "meaning": "injusticia, parcialidad"},
            {"kanji": "段階", "reading": "だんかい", "meaning": "etapa, fase, nivel (初期段階 fase inicial, 最終段階 fase final, 準備の段階 etapa de preparacion)"},
            {"kanji": "守る", "reading": "まもる", "meaning": "proteger, cumplir, respetar (normas, promesas tambien)"},
            {"kanji": "視野", "reading": "しや", "meaning": "campo de vision, perspectiva"},
            {"kanji": "偏見", "reading": "へんけん", "meaning": "prejuicio, sesgo, intolerancia"},
            {"kanji": "手続き", "reading": "てつづき", "meaning": "tramite"},
            {"kanji": "法律", "reading": "ほうりつ", "meaning": "ley"},
            {"kanji": "曖昧", "reading": "あいまい", "meaning": "impreciso, vago, ambiguo"},
            {"kanji": "文脈", "reading": "ぶんみゃく", "meaning": "contexto"},
            {"kanji": "世論", "reading": "よろん / せろん", "meaning": "opinion publica"},
            {"kanji": "被告", "reading": "ひこく", "meaning": "acusado, imputado"},
            {"kanji": "裁判", "reading": "さいばん", "meaning": "juicio"},
            {"kanji": "判決", "reading": "はんけつ", "meaning": "sentencia"},
            {"kanji": "有罪", "reading": "ゆうざい", "meaning": "culpable"},
            {"kanji": "無罪", "reading": "むざい", "meaning": "inocente"},
            {"kanji": "違法", "reading": "いほう", "meaning": "ilegal"},
            {"kanji": "合法", "reading": "ごうほう", "meaning": "legal"},
            {"kanji": "権利", "reading": "けんり", "meaning": "derecho"},
            {"kanji": "義務", "reading": "ぎむ", "meaning": "obligación moral"},
            {"kanji": "免許", "reading": "めんきょ", "meaning": "licencia (運転免許 licencia de conducir)"},
            {"kanji": "決定", "reading": "けってい", "meaning": "decisión"},
            {"kanji": "罰則", "reading": "ばっそく", "meaning": "código penal"},
            {"kanji": "違反", "reading": "いはん", "meaning": "infrigir, transgecion de la ley"},
            {"kanji": "規制", "reading": "きせい", "meaning": "regulación, control"},
            {"kanji": "契約", "reading": "けいやく", "meaning": "contrato, acuerdo"}
        ],
        "📄 Pasivos en Artículos": [
            {"kanji": "(と)期待される", "reading": "きたいされる", "meaning": "se espera que..."},
            {"kanji": "(と)見込まれて", "reading": "みこまれて", "meaning": "se prevee que..."},
            {"kanji": "評価される", "reading": "ひょうかされる", "meaning": "se reconoce su..., se valora..."},
            {"kanji": "注目されています", "reading": "ちゅうもくされています", "meaning": "estar recibiendo gran interés."}
        ],
        "💼 Comercial": [
            {"kanji": "品質", "reading": "ひんしつ", "meaning": "Calidad de un producto o materia"},
            {"kanji": "衛生", "reading": "えいせい", "meaning": "saneamiento, higiene"},
            {"kanji": "税抜き", "reading": "ぜいぬき", "meaning": "sin impuestos"},
            {"kanji": "税込み", "reading": "ぜいこみ", "meaning": "impuestos incluidos"},
            {"kanji": "別売り", "reading": "べつうり", "meaning": "se vende por separado, no incluido en el precio"},
            {"kanji": "広告", "reading": "こうこく", "meaning": "anuncios, publicidad"},
            {"kanji": "放送された", "reading": "ほうそうされた", "meaning": "ser transmitido, emitido"}
        ],
        "📍 Lugares": [
            {"kanji": "周辺", "reading": "しゅうへん", "meaning": "periferia, alrededores"},
            {"kanji": "廊下", "reading": "ろうか", "meaning": "pasillo"},
            {"kanji": "公共の場", "reading": "こうきょうのば", "meaning": "espacio publico"},
            {"kanji": "真ん中に", "reading": "まんなかに", "meaning": "en el centro, en el medio"},
            {"kanji": "距離", "reading": "きょり", "meaning": "distancia (física,relacion),intervalo,brecha"},
            {"kanji": "通う", "reading": "かよう", "meaning": "asistir, ir con regularidad, frecuentar un lugar"},
            {"kanji": "在宅", "reading": "ざいたく", "meaning": "estar en casa"},
            {"kanji": "在宅勤務", "reading": "ざいたくきんむ", "meaning": "trabajo desde casa"},
            {"kanji": "途中で", "reading": "とちゅうで", "meaning": "a mitad de camino, en medio de"},
            {"kanji": "観光地", "reading": "かんこうち", "meaning": "lugar turistico"},
            {"kanji": "近所", "reading": "きんじょ", "meaning": "barrio"},
            {"kanji": "舞台", "reading": "ぶたい", "meaning": "tarima, escenario"},
            {"kanji": "場面", "reading": "ばめん", "meaning": "escena, situacion de una pelicula, obra o vida real"},
            {"kanji": "食堂", "reading": "しょくどう", "meaning": "comedor"},
            {"kanji": "台所", "reading": "だいどころ", "meaning": "cocina"},
            {"kanji": "図書館", "reading": "としょかん", "meaning": "libreria"},
            {"kanji": "博物館", "reading": "はくぶつかん", "meaning": "museo"},
            {"kanji": "映画館", "reading": "えいがかん", "meaning": "cine"},
            {"kanji": "動物園", "reading": "どうぶつえん", "meaning": "zoologico"},
            {"kanji": "市役所", "reading": "しやくしょ", "meaning": "municipalidad"},
            {"kanji": "警察署", "reading": "けいさつしょ", "meaning": "comisaria"},
            {"kanji": "駐車場", "reading": "ちゅうしゃじょう", "meaning": "estacionamiento"},
            {"kanji": "交番", "reading": "こうばん", "meaning": "puesto de policia"},
            {"kanji": "高校", "reading": "こうこう", "meaning": "escuela secundaria superior"},
            {"kanji": "中学校", "reading": "ちゅうがっこう", "meaning": "escuela secundaria"},
            {"kanji": "小学校", "reading": "しょうがっこう", "meaning": "escuela primaria"},
            {"kanji": "パン屋", "reading": "ぱんや", "meaning": "panadera"},
            {"kanji": "肉屋", "reading": "にくや", "meaning": "carniceria"},
            {"kanji": "魚屋", "reading": "さかなや", "meaning": "pescaderia"},
            {"kanji": "銀行", "reading": "ぎんこう", "meaning": "banco"},
            {"kanji": "交差点", "reading": "こうさてん", "meaning": "cruce"},
            {"kanji": "通り", "reading": "とおり", "meaning": "calle"},
            {"kanji": "車道", "reading": "しゃどう", "meaning": "pista"},
            {"kanji": "歩道", "reading": "ほどう", "meaning": "vereda"},
            {"kanji": "角", "reading": "かど", "meaning": "esquina"},
            {"kanji": "道路", "reading": "どうろ", "meaning": "carretera"},
            {"kanji": "田舎", "reading": "いなか", "meaning": "campo,zona rural"},
            {"kanji": "工場", "reading": "こうじょう", "meaning": "fabrica"},
            {"kanji": "住所", "reading": "じゅうしょ", "meaning": "direccion"},
            {"kanji": "宿", "reading": "やど", "meaning": "alojamiento,hostal"},
            {"kanji": "設備", "reading": "せつび", "meaning": "instalación; infraestructura"}
        ],
        "🏛️ Política": [
            {"kanji": "撤回する", "reading": "てっかいする", "meaning": "retractarse"},
            {"kanji": "追及する", "reading": "ついきゅうする", "meaning": "cuestionar severamente, exigir responsabilidades"},
            {"kanji": "国会", "reading": "こっかい", "meaning": "parlamento nacional"},
            {"kanji": "政権", "reading": "せいけん", "meaning": "administración de un mandatario"},
            {"kanji": "野党", "reading": "やとう", "meaning": "oposición"},
            {"kanji": "代表", "reading": "だいひょう", "meaning": "representante, lider"},
            {"kanji": "与野党", "reading": "よやとう", "meaning": "partidos oficialistas y de oposición"},
            {"kanji": "給付", "reading": "きゅうふ", "meaning": "subsidio"},
            {"kanji": "公共交通機関", "reading": "こうきょうこうつうきかん", "meaning": "transporte publico"}
        ],
        "💻 Tecnología": [
            {"kanji": "基準", "reading": "きじゅん", "meaning": "normas o estándares"},
            {"kanji": "安全性", "reading": "あんぜんせい", "meaning": "seguridad o nivel de seguridad"},
            {"kanji": "満たす", "reading": "みたす", "meaning": "cumplir, satisfacer"},
            {"kanji": "能力", "reading": "のうりょく", "meaning": "habilidad, capacidad"},
            {"kanji": "操作する", "reading": "そうさする", "meaning": "operar, manejar una maquina, dispositivo o sistema"},
            {"kanji": "性能", "reading": "せいのう", "meaning": "eficiencia, rendimiento"},
            {"kanji": "権限", "reading": "けんげん", "meaning": "autoridad, facultades, permisos"},
            {"kanji": "仕組み", "reading": "しくみ", "meaning": "mecanismo, sistema, estructura"},
            {"kanji": "互換性", "reading": "ごかんせい", "meaning": "Compatibilidad"},
            {"kanji": "対応する", "reading": "たいおうする", "meaning": "soportar, adaptar"}
        ],
        "💼 Trabajo": [
            {"kanji": "急用", "reading": "きゅうよう", "meaning": "asunto urgente, compromiso o emergencia"},
            {"kanji": "機嫌", "reading": "きげん", "meaning": "estado de animo, humor"},
            {"kanji": "達成する", "reading": "たっせいする", "meaning": "lograr, alcanzar, cumplir una meta u objetivo"},
            {"kanji": "失敗する", "reading": "しっぱいする", "meaning": "fracasar, equivocarse (en un proyecto, plan o examen)"},
            {"kanji": "目指す", "reading": "めざす", "meaning": "aspirar, perseguir un sueño"},
            {"kanji": "退勤をする", "reading": "たいきんをする", "meaning": "salir del trabajo"},
            {"kanji": "目標", "reading": "もくひょう", "meaning": "meta, objetivo (especifico, corto plazo)"},
            {"kanji": "目的", "reading": "もくてき", "meaning": "propósito, meta (a largo plazo)"},
            {"kanji": "ストレスが溜まる", "reading": "ストレスがたまる", "meaning": "acumular estrés"},
            {"kanji": "遅れる", "reading": "おくれる", "meaning": "llegar tarde a..."},
            {"kanji": "環境", "reading": "かんきょう", "meaning": "ambiente (laboral, barrial), medio ambiente"},
            {"kanji": "締め切り", "reading": "しめきり", "meaning": "deadline"},
            {"kanji": "企画", "reading": "きかく", "meaning": "plan, proyecto"},
            {"kanji": "書類", "reading": "しょるい", "meaning": "documentos"},
            {"kanji": "厳しい", "reading": "きびしい", "meaning": "estricto"},
            {"kanji": "渡す", "reading": "わたす", "meaning": "entregar, pasar algo a la mano"},
            {"kanji": "職業", "reading": "しょくぎょう", "meaning": "oficio, profesion"},
            {"kanji": "手間", "reading": "てま", "meaning": "trabajo, esfuerzo"},
            {"kanji": "間に合う", "reading": "まにあう", "meaning": "llegar a tiempo a un lugar"},
            {"kanji": "さぼる", "reading": "さぼる", "meaning": "faltar a clases, holgazanear en el trabajo"},
            {"kanji": "手がける", "reading": "てがける", "meaning": "encargarse de, ocuparse de"},
            {"kanji": "運営", "reading": "うんえい", "meaning": "gestión"},
            {"kanji": "取り組む", "reading": "とりくむ", "meaning": "dedicarse a..."},
            {"kanji": "見送られる", "reading": "みおくられる", "meaning": "ser pospuesto, descartado, suspendido"},
            {"kanji": "稼ぐ", "reading": "かせぐ", "meaning": "ganar dinero"},
            {"kanji": "取り組み", "reading": "とりくみ", "meaning": "compromiso"},
            {"kanji": "利用者", "reading": "りようしゃ", "meaning": "usuario, cliente"},
            {"kanji": "部署", "reading": "ぶしょ", "meaning": "departamento, sección de una empresa"},
            {"kanji": "退職する", "reading": "たいしょくする", "meaning": "dejar un trabajo"},
            {"kanji": "面接", "reading": "めんせつ", "meaning": "entrevista"},
            {"kanji": "指摘", "reading": "してき", "meaning": "señalamiento, observación"},
            {"kanji": "残業", "reading": "ざんぎょう", "meaning": "horas extra"}
        ],
        "🏥 Medicina": [
            {"kanji": "診断", "reading": "しんだん", "meaning": "diagnostico, evaluación medica"},
            {"kanji": "検査を受ける", "reading": "けんさをうける", "meaning": "hacerse un examen, inspección o prueba medica"},
            {"kanji": "感染", "reading": "かんせん", "meaning": "infección, contagio"},
            {"kanji": "症状", "reading": "しょうじょう", "meaning": "sintomas"},
            {"kanji": "受診する", "reading": "じゅしんする", "meaning": "ir al medico para consulta"},
            {"kanji": "体のだるさ", "reading": "からだのだるさ", "meaning": "pesadez corporal"},
            {"kanji": "微熱", "reading": "びねつ", "meaning": "fiebre ligera"},
            {"kanji": "咳", "reading": "せき", "meaning": "tos"},
            {"kanji": "体重計", "reading": "たいじゅうけい", "meaning": "bascula, balanza"},
            {"kanji": "増進する", "reading": "ぞうしんする", "meaning": "estimular, promover"},
            {"kanji": "激痛が走る", "reading": "げきつうがはしる", "meaning": "recorrer un intenso dolor"},
            {"kanji": "防ぐ", "reading": "ふせぐ", "meaning": "evitar, prevenir, proteger"},
            {"kanji": "研究", "reading": "けんきゅう", "meaning": "investigación, estudio"},
            {"kanji": "結果", "reading": "けっか", "meaning": "resultado"},
            {"kanji": "体調", "reading": "たいちょう", "meaning": "estado de salud, condicion física"},
            {"kanji": "手術", "reading": "しゅじゅつ", "meaning": "cirugía u operación"},
            {"kanji": "治療", "reading": "ちりょう", "meaning": "tratamiento o terapia"},
            {"kanji": "消費する", "reading": "しょうひする", "meaning": "gastar, consumir"},
            {"kanji": "心拍", "reading": "しんぱく", "meaning": "latidos del corazon o ritmo cardiaco"},
            {"kanji": "怪我", "reading": "けが", "meaning": "lesión, herida o daño"},
            {"kanji": "依存症", "reading": "いぞんしょう", "meaning": "adicción"},
            {"kanji": "患者", "reading": "かんじゃ", "meaning": "paciente"}
        ]
    }

# -----------------------------------------------------------------------------
# INICIALIZACIÓN DEL ESTADO DE SESIÓN
# -----------------------------------------------------------------------------
if "category" not in st.session_state:
    st.session_state.category = list(st.session_state.vocab_categories.keys())[0]

if "quiz_queue" not in st.session_state:
    st.session_state.quiz_queue = random.sample(
        st.session_state.vocab_categories[st.session_state.category], 
        len(st.session_state.vocab_categories[st.session_state.category])
    )

if "total_category_len" not in st.session_state:
    st.session_state.total_category_len = len(st.session_state.vocab_categories[st.session_state.category])

if "current_item" not in st.session_state:
    st.session_state.current_item = st.session_state.quiz_queue.pop(0)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "show_hint" not in st.session_state:
    st.session_state.show_hint = False
if "options" not in st.session_state:
    st.session_state.options = []
if "show_kanji_temporary" not in st.session_state:
    st.session_state.show_kanji_temporary = False

def reset_queue_for_current_category():
    """Reinicia y baraja la cola de preguntas para la categoría actual."""
    cat = st.session_state.category
    words = st.session_state.vocab_categories[cat]
    st.session_state.quiz_queue = random.sample(words, len(words))
    st.session_state.total_category_len = len(words)

def update_category():
    cat = st.session_state.cat_selected
    st.session_state.category = cat
    reset_queue_for_current_category()
    next_question()

def on_mode_change():
    """Función que se ejecuta automáticamente al cambiar de modo de evaluación (hace el refresh del progreso)."""
    reset_queue_for_current_category()
    next_question()

def next_question():
    if not st.session_state.quiz_queue:
        reset_queue_for_current_category()
        st.toast("🎉 ¡Has completado toda la categoría! Comenzando de nuevo.")

    st.session_state.current_item = st.session_state.quiz_queue.pop(0)
    st.session_state.attempts = 0
    st.session_state.feedback = None
    st.session_state.show_hint = False
    st.session_state.show_kanji_temporary = False
    
    vocab = st.session_state.vocab_categories[st.session_state.category]
    item = st.session_state.current_item
    mode = st.session_state.get("mode_selected", "Modo 1: Kanji ➔ Significado")
    
    if "Modo 1" in mode:
        others = [x["meaning"] for x in vocab if x["meaning"] != item["meaning"]]
        opts = random.sample(others, min(3, len(others))) + [item["meaning"]]
        random.shuffle(opts)
        st.session_state.options = opts
    elif "Modo 3" in mode:
        others = [x["kanji"] for x in vocab if x["kanji"] != item["kanji"]]
        opts = random.sample(others, min(3, len(others))) + [item["kanji"]]
        random.shuffle(opts)
        st.session_state.options = opts

# -----------------------------------------------------------------------------
# BARRA LATERAL PARA GESTIÓN Y VISUALIZACIÓN DE PALABRAS
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Gestión de Vocabulario")

with st.sidebar.expander("📖 Ver palabras de la categoría"):
    view_cat = st.selectbox("Selecciona categoría a ver", list(st.session_state.vocab_categories.keys()), key="view_cat_select")
    st.write(f"**Total:** {len(st.session_state.vocab_categories[view_cat])} palabras")
    st.markdown("---")
    for item in st.session_state.vocab_categories[view_cat]:
        st.markdown(f"**{item['kanji']}** = {item['meaning']} *([{item['reading']}])*")

with st.sidebar.expander("➕ Añadir Categoría Nueva"):
    new_cat_name = st.text_input("Nombre de la Categoría (ej. ✈️ Viajes)")
    nc_kanji = st.text_input("Primer Kanji", key="nc_kanji")
    nc_reading = st.text_input("Lectura Hiragana", key="nc_reading")
    nc_meaning = st.text_input("Significado", key="nc_meaning")
    
    if st.button("Crear Categoría"):
        if new_cat_name.strip() and nc_kanji.strip() and nc_reading.strip() and nc_meaning.strip():
            if new_cat_name in st.session_state.vocab_categories:
                st.sidebar.error("¡Esa categoría ya existe!")
            else:
                clean_kanji = nc_kanji.strip()
                palabra_duplicada = False
                categoria_existente = ""
                for cat, words in st.session_state.vocab_categories.items():
                    if any(w["kanji"] == clean_kanji for w in words):
                        palabra_duplicada = True
                        categoria_existente = cat
                        break
                
                if palabra_duplicada:
                    st.sidebar.error(f"⚠️ La palabra '{clean_kanji}' ya está en '{categoria_existente}'.")
                else:
                    st.session_state.vocab_categories[new_cat_name] = [{
                        "kanji": clean_kanji,
                        "reading": nc_reading.strip(),
                        "meaning": nc_meaning.strip()
                    }]
                    st.sidebar.success(f"¡Categoría '{new_cat_name}' creada!")
                    st.rerun()
        else:
            st.sidebar.warning("Completa todos los campos.")

with st.sidebar.expander("📝 Añadir Palabra a Categoría"):
    target_cat = st.selectbox("Selecciona Categoría", list(st.session_state.vocab_categories.keys()), key="target_cat_add")
    np_kanji = st.text_input("Kanji / Palabra", key="np_kanji")
    np_reading = st.text_input("Lectura Hiragana", key="np_reading")
    np_meaning = st.text_input("Significado", key="np_meaning")
    
    if st.button("Guardar Palabra"):
        if np_kanji.strip() and np_reading.strip() and np_meaning.strip():
            clean_kanji = np_kanji.strip()
            palabra_duplicada = False
            categoria_existente = ""
            for cat, words in st.session_state.vocab_categories.items():
                if any(w["kanji"] == clean_kanji for w in words):
                    palabra_duplicada = True
                    categoria_existente = cat
                    break
            
            if palabra_duplicada:
                st.sidebar.error(f"⚠️ La palabra '{clean_kanji}' ya existe en '{categoria_existente}'.")
            else:
                st.session_state.vocab_categories[target_cat].append({
                    "kanji": clean_kanji,
                    "reading": np_reading.strip(),
                    "meaning": np_meaning.strip()
                })
                st.sidebar.success(f"¡Palabra añadida a {target_cat}!")
                if st.session_state.category == target_cat:
                    reset_queue_for_current_category()
                st.rerun()
        else:
            st.sidebar.warning("Completa todos los campos.")

# -----------------------------------------------------------------------------
# INTERFAZ PRINCIPAL
# -----------------------------------------------------------------------------
st.title("🇯🇵 Nihongo Quiz Multi-Categoría")

category_options = [f"{cat} ({len(words)} palabras)" for cat, words in st.session_state.vocab_categories.items()]
category_keys = list(st.session_state.vocab_categories.keys())

if st.session_state.category not in category_keys:
    st.session_state.category = category_keys[0]

current_display_default = f"{st.session_state.category} ({len(st.session_state.vocab_categories[st.session_state.category])} palabras)"
try:
    default_index = category_options.index(current_display_default)
except ValueError:
    default_index = 0

selected_display = st.selectbox(
    "Selecciona la categoría de vocabulario:",
    category_options,
    index=default_index,
    key="cat_display_selected"
)

selected_index = category_options.index(selected_display)
real_category_key = category_keys[selected_index]

if st.session_state.category != real_category_key:
    st.session_state.cat_selected = real_category_key
    update_category()

modos = [
    "Modo 1: Kanji ➔ Significado",
    "Modo 2: Kanji ➔ Lectura en Hiragana",
    "Modo 3: Audio ➔ Kanji correcto",
    "Modo 4: Lectura ➔ Dibujar Kanji (Teclado)"
]

selected_mode = st.selectbox(
    "Selecciona el modo de evaluación:",
    modos,
    key="mode_selected",
    on_change=on_mode_change
)

if not st.session_state.options:
    next_question()

item = st.session_state.current_item

completadas = st.session_state.total_category_len - len(st.session_state.quiz_queue) - 1
if completadas < 0:
    completadas = 0

st.caption(f"🏆 Puntuación: **{st.session_state.score}** | Categoría: **{st.session_state.category}** | Progreso de ronda: **{completadas} de {st.session_state.total_category_len}** palabras")
st.divider()

# -----------------------------------------------------------------------------
# LÓGICA DE LOS 4 MODOS
# -----------------------------------------------------------------------------

# --- MODO 1: KANJI ➔ SIGNIFICADO ---
if "Modo 1" in selected_mode:
    st.subheader("¿Cuál es el significado correcto?")
    st.markdown(f'<div class="kanji-display">{item["kanji"]}</div>', unsafe_allow_html=True)
    
    for idx, opt in enumerate(st.session_state.options):
        if st.button(opt, key=f"m1_btn_{idx}"):
            if opt == item["meaning"]:
                st.session_state.feedback = "correct"
                st.session_state.score += 1
            else:
                st.session_state.attempts += 1
                if st.session_state.attempts == 1:
                    st.session_state.feedback = "retry"
                    st.session_state.show_hint = True
                else:
                    st.session_state.feedback = "failed"

# --- MODO 2: KANJI ➔ LECTURA EN HIRAGANA ---
elif "Modo 2" in selected_mode:
    st.subheader("Escribe la lectura exacta en Hiragana:")
    st.markdown(f'<div class="kanji-display">{item["kanji"]}</div>', unsafe_allow_html=True)
    
    user_input = st.text_input("Lectura en Hiragana:", key="m2_input")
    
    if st.button("Comprobar lectura", key="m2_submit"):
        if user_input.strip() == item["reading"]:
            st.session_state.feedback = "correct"
            st.session_state.score += 1
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts == 1:
                st.session_state.feedback = "retry"
                st.session_state.show_hint = True
            else:
                st.session_state.feedback = "failed"

# --- MODO 3: AUDIO ➔ KANJI CORRECTO ---
elif "Modo 3" in selected_mode:
    st.subheader("Escucha el audio y selecciona el Kanji correcto:")
    
    if st.button("🔊 Reproducir Audio", key="play_audio"):
        tts = gTTS(text=item["kanji"], lang="ja")
        tts.save("temp_quiz.mp3")
        st.audio("temp_quiz.mp3", format="audio/mp3")
        
    st.write("---")
    for idx, opt in enumerate(st.session_state.options):
        if st.button(opt, key=f"m3_btn_{idx}"):
            if opt == item["kanji"]:
                st.session_state.feedback = "correct"
                st.session_state.score += 1
            else:
                st.session_state.attempts += 1
                if st.session_state.attempts == 1:
                    st.session_state.feedback = "retry"
                    st.session_state.show_hint = True
                else:
                    st.session_state.feedback = "failed"

# --- MODO 4: LECTURA EN HIRAGANA ➔ DIBUJAR KANJI ---
elif "Modo 4" in selected_mode:
    st.subheader("Dibuja o introduce el Kanji con tu teclado táctil:")
    
    if st.session_state.show_kanji_temporary:
        st.markdown(f'<div class="kanji-display" style="color: #E11D48;">{item["kanji"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="hiragana-display">{item["reading"]} ({item["meaning"]})</div>', unsafe_allow_html=True)
        
    st.caption("💡 Tip: En el teclado de tu celular, usa el icono de escritura a mano para dibujar el kanji.")
    
    user_kanji = st.text_input("Kanji reconocido:", key="m4_input")
    
    if st.button("Comprobar Kanji", key="m4_submit"):
        if user_kanji.strip() == item["kanji"]:
            st.session_state.feedback = "correct"
            st.session_state.score += 1
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts == 1:
                st.session_state.feedback = "retry"
                st.session_state.show_hint = True
                st.session_state.show_kanji_temporary = True
                st.rerun()
            else:
                st.session_state.feedback = "failed"

# -----------------------------------------------------------------------------
# RETROALIMENTACIÓN Y PISTAS (SISTEMA DE 2 INTENTOS)
# -----------------------------------------------------------------------------
if st.session_state.feedback == "correct":
    st.success(f"¡Correcto! 🎉 La respuesta es **{item['kanji']}** ({item['reading']}) - {item['meaning']}")
    if st.button("Siguiente Pregunta ➔", key="next_correct"):
        next_question()
        st.rerun()

elif st.session_state.feedback == "retry":
    st.warning("⚠️ Respuesta incorrecta. ¡Tienes 1 intento más!")
    if st.session_state.show_hint:
        if "Modo 2" in selected_mode:
            two_syllables = item["reading"][:2] if len(item["reading"]) >= 2 else item["reading"]
            st.info(f"💡 **Pista:** Empieza con **{two_syllables}...**")
        elif "Modo 3" in selected_mode:
            st.info(f"💡 **Pista (Lectura en Hiragana):** {item['reading']}")
        elif "Modo 4" in selected_mode:
            st.info("💡 **Pista:** Observa el Kanji arriba durante 5 segundos...")
            time.sleep(5)
            st.session_state.show_kanji_temporary = False
            st.rerun()
        else:
            st.info(f"💡 **Pista:** La lectura es {item['reading']}")

elif st.session_state.feedback == "failed":
    st.error(f"❌ Intentos agotados. La respuesta correcta era: **{item['kanji']}** ({item['reading']}) - {item['meaning']}")
    if st.button("Siguiente Pregunta ➔", key="next_failed"):
        next_question()
        st.rerun()
