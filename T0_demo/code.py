# coding=utf-8
# 
class TibetStr:
    def __init__(self, jcz_path):
        self.jcz_path = jcz_path

    def jichuzi_yuanyin(self):
        """基础字+元音"""
        yuanyin_list = ['ི', 'ུ', 'ེ', 'ོ']
        result = []
        for zi in self.jcz_path:
            result.append(zi)
            for yy in yuanyin_list:
                result.append(zi + yy)
        return result, len(result)

    def jichuzi_houjiazi(self):
        """基础字+后加字"""
        houjiazi_list = ['ག', 'ང', 'ད', 'ན', 'བ', 'མ', 'ར', 'ལ', 'ས']
        base_list = self.jichuzi_yuanyin()[0]
        result = []
        for zi in base_list:
            for h in houjiazi_list:
                result.append(zi + h)
        return result, len(result)

    def jcz_zhjz_sa(self):
        """基础字+后加字+再后加字ས"""
        base_list = self.jichuzi_houjiazi()[0]
        result = [zi + "ས" for zi in base_list if zi[-1] in {"ག", "ང", "བ", "མ"}]
        return result, len(result)

    def jcz_zhjz_da(self):
        """基础字+后加字+再后加字ད"""
        base_list = self.jichuzi_houjiazi()[0]
        result = [zi + "ད" for zi in base_list if zi[-1] in {"ན", "ར", "ལ"}]
        return result, len(result)

    def jichuzi_ha(self):
        """基础字+འ"""
        result = []
        for zi in self.jcz_path:
            if len(zi) == 2 and zi[0] in "གདབམའ" and zi[-1] not in "ྱྲླྭ":
                result.append(zi + "འ")
        return result, len(result)

    def fuhao(self):
        """符号"""
        symbols = ["ི", "ུ", "ེ", "ོ", "༄", "།", "་"]
        return symbols, len(symbols)

    def tibet_sum(self):
        """全藏字组合"""
        all_words = []
        all_words.extend(self.jichuzi_yuanyin()[0])
        all_words.extend(self.jichuzi_houjiazi()[0])
        all_words.extend(self.jcz_zhjz_sa()[0])
        all_words.extend(self.jcz_zhjz_da()[0])
        all_words.extend(self.jichuzi_ha()[0])
        all_words.extend(self.fuhao()[0])
        return all_words, f"全藏字总共有{len(all_words)}个字"

if __name__ == '__main__':
    jcz_str = [
        # ...（原有的藏文基础字列表，省略，保持不变）...
        'ཀ', 'ཁ', 'ག', 'ང', 'ཅ', 'ཆ', 'ཇ', 'ཉ', 'ཏ', 'ཐ', 'ད', 'ན', 'པ', 'ཕ', 'བ', 'མ', 'ཙ', 'ཚ', 'ཛ', 'ཝ', 'ཞ', 'ཟ', 'འ', 'ཡ', 'ར', 'ལ', 'ཤ', 'ས', 'ཧ', 'ཨ', 'རྐ', 'རྒ', 'རྔ', 'རྗ', 'རྙ', 'རྟ', 'རྡ', 'རྣ', 'རྦ', 'རྨ', 'རྩ', 'རྫ', 'ལྐ', 'ལྒ', 'ལྔ', 'ལྕ', 'ལྗ', 'ལྟ', 'ལྡ', 'ལྤ', 'ལྦ', 'ལྷ', 'སྐ', 'སྒ', 'སྔ', 'སྙ', 'སྟ', 'སྡ', 'སྣ', 'སྤ', 'སྦ', 'སྨ', 'སྩ', 'ཀྱ', 'ཁྱ', 'གྱ', 'པྱ', 'ཕྱ', 'བྱ', 'མྱ', 'ཀྲ', 'ཁྲ', 'གྲ', 'ཏྲ', 'ཐྲ', 'དྲ', 'པྲ', 'ཕྲ', 'བྲ', 'སྲ', 'ཧྲ', 'ཀླ', 'གླ', 'བླ', 'ཟླ', 'རླ', 'སླ', 'རྐྱ', 'རྒྱ', 'རྨྱ', 'སྐྱ', 'སྒྱ', 'སྤྱ', 'སྦྱ', 'སྨྱ', 'སྐྲ', 'སྒྲ', 'སྤྲ', 'སྦྲ', 'སྨྲ', 'སྣྲ', 'གཅ', 'གཙ', 'གཉ', 'གཏ', 'གད', 'གན', 'གཞ', 'གཟ', 'གཡ', 'གཤ', 'གས', 'དཀ', 'དག', 'དང', 'དཔ', 'དབ', 'དམ', 'བཀ', 'བག', 'བཅ', 'བཙ', 'བཏ', 'བད', 'བཞ', 'བཟ', 'བཤ', 'བས', 'མཁ', 'མག', 'མང', 'མཆ', 'མཇ', 'མཉ', 'མཐ', 'མད', 'མན', 'མཚ', 'མཛ', 'འཁ', 'འག', 'འཆ', 'འཇ', 'འཐ', 'འད', 'འཕ', 'འབ', 'འཚ', 'འཛ', 'དཀྱ', 'དགྱ', 'དཔྱ', 'དབྱ', 'དམྱ', 'དཀྲ', 'དགྲ', 'དཔྲ', 'དབྲ', 'བཀྲ', 'བགྲ', 'བསྲ', 'བཀླ', 'བཟླ', 'བརླ', 'བསླ', 'མཁྱ', 'མཁྲ', 'མགྱ', 'མགྲ', 'འཁྲ', 'འགྲ', 'འཕྲ', 'འབྲ', 'འདྲ', 'འཁྱ', 'འགྱ', 'འཕྱ', 'འབྱ', 'བརྐ', 'བརྒ', 'བརྔ', 'བརྗ', 'བརྙ', 'བརྟ', 'བརྡ', 'བརྣ', 'བརྩ', 'བརྫ', 'བལྟ', 'བལྡ', 'བསྐ', 'བསྒ', 'བསྔ', 'བསྙ', 'བསྟ', 'བསྡ', 'བསྣ', 'བསྩ', 'བརྐྱ', 'བརྒྱ', 'བཀྱ', 'བགྱ', 'བསྐྱ', 'བསྒྱ', 'བསྐྲ', 'བསྒྲ', 'ཀྭ', 'ཁྭ', 'གྭ', 'ཉྭ', 'དྭ', 'ཚྭ', 'ཞྭ', 'ཟྭ', 'རྭ', 'ལྭ', 'ཤྭ', 'ཧྭ', 'རྩྭ', 'གྲྭ', 'ཕྱྭ'
    ]
    tibet = TibetStr(jcz_str)
    all_words, summary = tibet.tibet_sum()
    print(f"{all_words},\n{summary}")
    with open("全藏字.txt", "w", encoding="utf-8") as ff:
        for word in all_words:
            ff.write(word + "\n")