        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 15px;">
                        <i>P(X &le; {self.variable_2_display})</i> = 
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr><td align="center" style="font-size: 18px; padding-bottom: 2px;">{self.variable_2_display}</td></tr>
                            <tr><td align="center" style="font-size: 40px; line-height: 0.8;">&sum;</td></tr>
                            <tr><td align="center" style="font-size: 18px; padding-top: 8px;"><i>i=0</i></td></tr>
                        </table>
                    </td>
                    
                    <td valign="middle" style="padding-left: 10px;">
                        <table cellpadding="0" cellspacing="0" style="font-size: 28px;">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0px 10px 4px 10px;">
                                    {self.variable_1_display}<sup>i</sup> &middot; <i>e</i><sup>-{self.variable_1_display}</sup>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 4px 10px 0px 10px;">
                                    i!
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 20px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)
