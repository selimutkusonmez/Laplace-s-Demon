
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" <style = "font-size : 30px;" >
                <tr>
                    <td valign="middle" style="padding-right: 15px;">
                        <i>F({self.variable_4_display})</i> = <i>P(X &le; {self.variable_4_display})</i> = 
                    </td>
                    
                    <td valign="middle" style="padding-right: 10px;">
                        <table cellpadding="0" cellspacing="0" style="font-size: 32px;">
                            <tr><td align="center" style="border-bottom: 2px solid currentColor;">1</td></tr>
                            <tr><td align="center">2</td></tr>
                        </table>
                    </td>

                    <td valign="middle" style="font-size: 55px; font-weight: lighter;">(</td>
                    <td valign="middle" style="padding: 0 5px;">
                        1 + erf
                    </td>
                    
                    <td valign="middle" style="font-size: 55px; font-weight: lighter;">(</td>
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0" style="font-size: 28px;">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 5px 3px 5px;">
                                    ln {self.variable_4_display} &minus; {self.variable_1_display}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 3px 5px 0 5px;">
                                    {self.variable_2_display}&radic;<span style="text-decoration: overline;">2</span>
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td valign="middle" style="font-size: 55px; font-weight: lighter;">)</td>
                    <td valign="middle" style="font-size: 55px; font-weight: lighter;">)</td>

                    <td valign="middle" style="padding-left: 25px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

        