

        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 10px;"><i>F({self.variable_1_display})</i> = </td>
                    
                    <td valign="middle" style="font-size: 200px; font-weight: lighter; padding-right: 15px; padding-bottom: 10px;">{{</td>

                    <td valign="middle">
                        <table cellpadding="4" cellspacing="0" style="font-size: 24px;">
                            <tr>
                                <td>0 ,</td>
                                <td style="padding-left: 20px;">{self.variable_1_display} &lt; {self.variable_2_display}</td>
                            </tr>
                            <tr>
                                <td valign="middle">
                                    <table cellpadding="0" cellspacing="0">
                                        <tr><td align="center" style="border-bottom: 2px solid currentColor;">{self.variable_1_display} &minus; {self.variable_2_display}</td></tr>
                                        <tr><td align="center">{self.variable_3_display} &minus; {self.variable_2_display}</td></tr>
                                    </table>
                                </td>
                                <td valign="middle" style="padding-left: 20px;">{self.variable_2_display} &le; {self.variable_1_display} &le; {self.variable_3_display}</td>
                            </tr>
                            <tr>
                                <td>1 ,</td>
                                <td style="padding-left: 20px;">{self.variable_1_display} &gt; {self.variable_3_display}</td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 30px;">= {self.current_result}</td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

