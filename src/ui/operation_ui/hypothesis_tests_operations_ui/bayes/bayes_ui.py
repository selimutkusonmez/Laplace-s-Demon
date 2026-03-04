        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 15px;">
                        P(A|B) = 
                    </td>
                    <td align="center" valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 10px 4px 10px;">
                                    {self.variable_2_display} &middot; {self.variable_1_display}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 6px 10px 0 10px;">
                                    {self.variable_3_display}
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td valign="middle" style="padding-left: 20px;">
                        = 
                    </td>
                    <td valign="middle" style="padding-left: 10px; line-height: 1.2;">
                        {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

