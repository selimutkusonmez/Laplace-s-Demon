
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 22px;">
                        <i>F({self.variable_4_display})</i> = 
                    </td>
                    
                    <td valign="middle" style="padding-right: 15px;">
                        <table cellpadding="0" cellspacing="0" style="font-size: 36px;">
                            <tr>
                                <td align="center" style="border-bottom: 3px solid currentColor; padding: 0px 12px 6px 12px;">
                                    1
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 6px 12px 0px 12px;">
                                    &radic;<span style="text-decoration: overline;">2&pi;</span>{self.variable_2_display}
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-right: 10px;">
                        <table cellpadding="0" cellspacing="0">
                            <tr><td align="center" style="font-size: 24px; padding-bottom: 0px;">{self.variable_4_display}</td></tr>
                            <tr><td align="center" style="font-size: 65px; line-height: 0.8;">&int;</td></tr>
                            <tr><td align="center" style="font-size: 24px; padding-top: 0px;">&minus;&infin;</td></tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 5px; font-size: 51px;">
                        <i>e</i>
                    </td>

                    <td valign="top" style="padding-top: 15px;">
                        <table cellpadding="0" cellspacing="0" style="font-size: 27px;">
                            <tr>
                                <td rowspan="2" valign="middle" style="padding-right: 8px; font-size: 33px;">
                                    &minus;
                                </td>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0px 6px 3px 6px;">
                                    (<i>t</i> &minus; {self.variable_1_display})<sup>2</sup>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 3px 6px 0px 6px;">
                                    2&times;{self.variable_2_display}<sup>2</sup>
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 15px; font-size: 40px;">
                        <i>dt</i>
                    </td>

                    <td valign="middle" style="padding-left: 30px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)


        